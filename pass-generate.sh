#!/bin/bash

set -e
set -o pipefail

QUERY=$1
PATH=/usr/local/bin:$PATH

pass generate "$QUERY" 16 | tail -n1 | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | awk 'BEGIN{ORS=""} {print; exit}'
