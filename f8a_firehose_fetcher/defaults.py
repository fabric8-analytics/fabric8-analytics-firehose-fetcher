#!/usr/bin/env python3

import os

STREAM_URL = os.environ.get('FIREHOSE_STREAM_URL', 'https://firehose.libraries.io/events')
ENABLE_SCHEDULING = os.environ.get('ENABLE_SCHEDULING', '1') in ('1', 'True', 'true')
PROBE_FILE_LOCATION = "/tmp/firehose-fetcher/liveness.txt"
