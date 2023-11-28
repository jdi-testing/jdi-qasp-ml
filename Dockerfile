FROM python:3.7.9-slim-buster

RUN apt-get update -y && \
    apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    apt-get dist-upgrade

RUN apt install -y curl wget mc gcc make

RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg wget curl unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* && \
    CHROME_VERSION=$(google-chrome --product-version) && \
    wget -q --continue -P /chromedriver "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/ && \
    rm -rf /chromedriver

ENV APP_HOME=/jdi-qasp-ml
WORKDIR ${APP_HOME}

COPY Pipfile* ${APP_HOME}/

RUN pip install -U pip && \
    pip install pipenv

RUN pipenv install --ignore-pipfile --system --deploy

COPY . ${APP_HOME}

ENV PYTHONPATH=${PYTHONPATH}:/jdi-qasp-ml
