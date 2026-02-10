FROM ubuntu:plucky

RUN apt-get update \
 && apt-get install -y software-properties-common gpg dh-virtualenv devscripts debhelper dh-python python3-virtualenv devscripts python3-setuptools pybuild-plugin-pyproject python3-pip \
 && apt-get clean \
 && pip install uv hatchling --break-system-packages

COPY build_in_docker.sh /
