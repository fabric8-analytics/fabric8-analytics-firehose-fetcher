import docker


def before_all(context):
    client = docker.from_env(version="auto")
    context.firehose_container = client.containers.run(
        "f8a-firehose-fetcher-tests",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )


def after_all(context):
    context.firehose_container.kill()
