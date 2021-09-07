FROM continuumio/miniconda3
EXPOSE 5000/tcp
EXPOSE 5000/udp

RUN apt-get update -y && apt-get install -y apt-utils && apt-get upgrade -y && apt-get install -y locales && apt-get dist-upgrade
RUN apt install -y curl wget mc
COPY docker-environment.yml ${HOME}/environment.yml
RUN conda env update -n base -f environment.yml

ENV USER_NAME=jdi-ml
ENV HOME=/home/${USER_NAME}
WORKDIR ${HOME}
RUN useradd -d ${HOME} -m ${USER_NAME}
RUN chown ${USER_NAME}:${USER_NAME} ${HOME}

USER ${USER_NAME}

RUN mkdir ${HOME}/utils
RUN mkdir ${HOME}/html
RUN mkdir ${HOME}/model
RUN mkdir -p ${HOME}/dataset/df
RUN mkdir -p ${HOME}/flask-temp-storage
COPY dataset/classes.txt ${HOME}/dataset/classes.txt
COPY model model
COPY MUI_model MUI_model
COPY utils utils
COPY templates templates
COPY main.py ${HOME}/main.py

USER root
RUN echo "#!/bin/bash" >> /entrypoint.sh
RUN echo "cd ${HOME}" >> /entrypoint.sh
RUN echo "uwsgi --socket 0.0.0.0:5000 --process=5 --protocol=http -w main:api" >> /entrypoint.sh
RUN chmod a+x /entrypoint.sh
RUN MODEL_VERSION=`date +%Y-%m-%d-%H.%M.%S`; mkdir -p ${HOME}/model/version; touch ${HOME}/model/version/${MODEL_VERSION};  

USER ${USER_NAME}
ENTRYPOINT [ "/entrypoint.sh" ]


