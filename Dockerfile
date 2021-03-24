FROM continuumio/miniconda3
EXPOSE 5000/tcp
EXPOSE 5000/udp

ENV HOME=/root

RUN apt-get update -y && apt-get install -y apt-utils && apt-get upgrade -y && apt-get install -y locales && apt-get dist-upgrade
COPY docker-environment.yml ${HOME}/environment.yml

WORKDIR ${HOME}

RUN conda env update -n base -f environment.yml
RUN mkdir ${HOME}/utils
RUN mkdir ${HOME}/model
RUN mkdir -p ${HOME}/dataset/df
RUN mkdir -p ${HOME}/flask-temp-storage
COPY dataset/classes.txt ${HOME}/dataset/classes.txt
COPY model model
COPY utils utils

RUN apt install -y curl mc

COPY main.py ${HOME}/main.py

CMD ["python", "./main.py"]
