import docker


def before_all(context):
    client = docker.from_env(version="auto")
    context.firehose_container = client.containers.run(
        "f8a-firehose-fetcher-tests",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )


def after_all(context):
    try:
        context.firehose_container.kill()
    except docker.errors.APIError:
        print(context.firehose_container.logs())
        raise
