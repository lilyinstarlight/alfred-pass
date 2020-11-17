#!/bin/bash

set -e
set -o pipefail

QUERY=$1
PATH=/usr/local/bin:$PATH

pass otp "$QUERY" | awk 'BEGIN{ORS=""} {print; exit}'
