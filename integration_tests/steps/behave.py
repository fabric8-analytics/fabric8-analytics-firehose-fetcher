from behave import *
import docker
import sseclient
import requests
import json

from f8a_firehose_fetcher.defaults import STREAM_URL


@given('Container is running')
def step_impl(context):
    client = docker.from_env()
    context.firehose_container = client.containers.run(
        "registry.devshift.net/fabric8-analytics/firehose-fetcher",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )
    print(context.firehose_container.status)
    assert context.firehose_container.status == 'created'


@when('Got three Firehose events')
def step_impl(context):
    response = requests.get(STREAM_URL, stream=True, timeout=30)
    sse = sseclient.SSEClient(response)
    context.events = []
    for event in sse.events():
        if len(context.events) == 3:
            break
        data = json.loads(event.data)
        context.events.append((data['platform'].lower(), data['name'], data['version']))


@then('Check container logs for received events')
def step_impl(context):
    for e in context.events:
        if "'{}':'{}':'{}'".format(e[0], e[1], e[2]) in\
                context.firehose_container.logs().strip().decode('utf-8'):
            continue
        else:
            assert False
