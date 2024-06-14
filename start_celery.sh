#!/bin/bash

CORES_TO_USE=$(($(nproc)-2>0?$(nproc)-2:1))
echo "Celery will use $CORES_TO_USE cores"
celery -A app.celery_app:celery_app worker -l info --concurrency $CORES_TO_USE
