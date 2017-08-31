from behave import *


@given('Container is running')
def step_impl(context):
    assert context.firehose_container.status == 'created'


@then('Check container logs for "{count}" received events')
def step_impl(context, count):
    event_count = 0
    for e in context.firehose_container.logs(stream=True):
        if "Received event for package" in e.decode('utf-8'):
            event_count = event_count + 1

        if event_count >= int(count):
            print(event_count)
            break
