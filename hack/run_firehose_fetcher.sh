#!/usr/bin/env bash

set -ex

# This script is from worker image and it's required until
# names for environment variables are unified
source /usr/bin/env.sh

exec cli
