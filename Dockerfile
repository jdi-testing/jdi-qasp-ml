FROM python:3.7.9-slim-buster

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    apt-get dist-upgrade

RUN apt install -y curl wget mc gcc make

ENV APP_HOME=/jdi-qasp-ml
WORKDIR ${APP_HOME}

COPY Pipfile* ./

RUN pip install -U pip && \
    pip install pipenv

RUN pipenv install --ignore-pipfile --system --deploy

COPY . ./

RUN chmod +x start_celery.sh

ENV PYTHONPATH=${PYTHONPATH}:/jdi-qasp-ml
