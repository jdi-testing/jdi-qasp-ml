#!/bin/bash

CORES_TOTAL=$(nproc)
CORES_TO_USE=$((CORES_TOTAL - 2))

if [[ $CORES_TOTAL -le 2 ]]; then
  CORES_TO_USE=$CORES_TOTAL
fi

CORES_AVAILABLE=$(seq -s, 0 $((CORES_TO_USE - 1)))

export CORES_API=$CORES_AVAILABLE
export CORES_CELERY=$CORES_AVAILABLE
export CORES_REDIS=$CORES_AVAILABLE
export CORES_MONGODB=$CORES_AVAILABLE

docker-compose -f docker-compose.yaml up
