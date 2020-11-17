#!/bin/bash

set -e
set -o pipefail

QUERY=$1
PATH=/usr/local/bin:$PATH

PINENTRY_USER_DATA=gui pass show "$QUERY" | awk 'BEGIN{ORS=""} {print; exit}'
