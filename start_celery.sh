#!/bin/bash

CORES_TO_USE=$(($(nproc)-2>0?$(nproc)-2:1))
echo $CORES_TO_USE
celery -A app.celery_app:celery_app worker -l info --concurrency $CORES_TO_USE
