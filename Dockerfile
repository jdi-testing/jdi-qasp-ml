FROM python:3.7.9-slim-buster

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    apt-get dist-upgrade

RUN apt install -y curl wget mc gcc make gnupg gnupg2 gnupg1

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
RUN wget -N https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

ENV APP_HOME=/jdi-qasp-ml
WORKDIR ${APP_HOME}

COPY Pipfile* ${APP_HOME}/

RUN pip install -U pip && \
    pip install pipenv

RUN pipenv install --ignore-pipfile --system --deploy

COPY . ${APP_HOME}

ENV PYTHONPATH=${PYTHONPATH}:/jdi-qasp-ml

