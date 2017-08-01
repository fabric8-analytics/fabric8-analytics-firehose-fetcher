#!/usr/bin/env bash

set -ex
# As in worker, we need inject environment setup
DIR=$(dirname "${BASH_SOURCE[0]}")
source $DIR/env.sh

exec cli