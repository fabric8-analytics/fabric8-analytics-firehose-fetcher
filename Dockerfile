FROM registry.centos.org/centos/centos:7
MAINTAINER Pavel Kajaba <pavel@redhat.com>

ENV LANG=en_US.UTF-8 \
    F8A_WORKER_VERSION=9734983

RUN useradd coreapi

RUN yum install -y epel-release && \
    yum install -y python34-devel python34-pip gcc git && \
    yum clean all

COPY ./ /tmp/f8a_firehose-fetcher/
RUN pushd /tmp/f8a_firehose-fetcher/ &&\
  pip3 install . &&\
  pip3 install --upgrade --no-binary :all: protobuf && pip3 install git+https://github.com/fabric8-analytics/fabric8-analytics-worker.git@${F8A_WORKER_VERSION} &&\
  popd &&\
  rm -rf /tmp/firehose_fetcher

COPY hack/run_firehose_fetcher.sh /usr/bin/

USER coreapi
CMD ["/usr/bin/run_firehose_fetcher.sh"]

