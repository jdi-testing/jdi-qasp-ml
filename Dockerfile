FROM python:3.7.9-slim-buster

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    apt-get dist-upgrade

RUN apt install -y curl wget mc gcc

ENV APP_HOME=/app
WORKDIR ${APP_HOME}

COPY . ${APP_HOME}

RUN pip install -U pip && \
    pip install pipenv

RUN pipenv install --ignore-pipfile --system --deploy

ENV PYTHONPATH=${PYTHONPATH}:/app

RUN MODEL_VERSION=`date +%Y-%m-%d-%H.%M.%S`; mkdir -p ${APP_HOME}/model/version; touch ${APP_HOME}/model/version/${MODEL_VERSION};

RUN mkdir ${HOME}/html
RUN mkdir -p ${HOME}/MUI_model/tmp
