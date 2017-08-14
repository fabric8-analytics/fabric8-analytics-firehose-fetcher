#!/usr/bin/env python3

import logging
import requests
import json
import sseclient
import os
import sys
import signal
import psutil
import time

from selinon import run_flow
from f8a_worker.setup_celery import init_celery, init_selinon
from .defaults import STREAM_URL, ENABLE_SCHEDULING, PROBE_FILE_LOCATION

logger = logging.getLogger(__name__)


def handler(signum, frame):
    logger.warning("Liveness probe - trying to schedule the livenessFlow")
    if ENABLE_SCHEDULING:
        run_flow('livenessFlow', [None])
    else:
        logger.warning("Liveness probe - livenessFlow"
                       " did not run since selinon is not initialized")

    basedir = os.path.dirname(PROBE_FILE_LOCATION)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(PROBE_FILE_LOCATION, 'a'):
        logger.warning("Liveness probe - created file")
        os.utime(PROBE_FILE_LOCATION, None)

    logger.warning("Liveness probe - finished")


def run_liveness():
    # Remove all temp files to ensure that there are no leftovers
    if os.path.isfile(PROBE_FILE_LOCATION):
        os.remove(PROBE_FILE_LOCATION)

    for pid in psutil.process_iter():
        if pid.pid == 1:
            pid.send_signal(signal.SIGUSR1)
            time.sleep(5)

    sys.exit(0 if os.path.isfile(PROBE_FILE_LOCATION) else 1)


class FirehoseFetcher(object):
    """ Basic class which handles firehose events"""

    def __init__(self):
        self.log = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging_handler = logging.StreamHandler(sys.stdout)
        logging_handler.setFormatter(formatter)
        self.log.addHandler(logging_handler)

        if ENABLE_SCHEDULING:
            init_celery(result_backend=False)
            init_selinon()

    def analyses_selinon_flow(self, name, version, ecosystem):
        """Run Selinon flow for analyses.
        :param name: name of the package to analyse
        :param version: package version
        :param ecosystem: package ecosystem
        :return: dispatcher ID serving flow
        """

        node_args = {
            'ecosystem': ecosystem,
            'name': name,
            'version': version
        }

        self.log.debug("Scheduling Selinon flow '%s' with node_args: '%s'", 'bayesianFlow', node_args)
        return run_flow('bayesianFlow', node_args)

    def run(self):
        self.log.info("Initializing Server Side Events client")

        response = requests.get(STREAM_URL, stream=True, timeout=30)
        if response.status_code != requests.codes.ok:
            self.log.warning("Unable to retrieve connection with '%s'", STREAM_URL)
            response.raise_for_status()
        self.log.debug("Connection with '%s' established", STREAM_URL)

        signal.signal(signal.SIGUSR1, handler)
        self.log.info("Registered signal handler for liveness probe")

        client = sseclient.SSEClient(response)
        for event in client.events():
            data = json.loads(event.data)
            try:
                name = data['name']
                version = data['version']
                ecosystem = data['platform'].lower()
            except KeyError:
                self.log.debug("Event is missing one of required keys, skipping it")
                continue

            self.log.warning("Received event for package '%s' from ecosystem '%s'", name, ecosystem)
            # For current set of ecosystems (nuget, pypi, maven and npm) calling lower is sufficient
            if ecosystem in {'nuget', 'pypi', 'maven', 'npm'} and ENABLE_SCHEDULING:
                self.analyses_selinon_flow(name, version, ecosystem)
            else:
                self.log.debug("Ecosystem '%s' is not currently supported", ecosystem)
