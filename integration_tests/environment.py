import docker


def before_all(context):
    client = docker.from_env(version="auto")
    context.firehose_container = client.containers.run(
        "registry.devshift.net/fabric8-analytics/firehose-fetcher",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )


def after_all(context):
    context.firehose_container.kill()
