FROM python:3.7
MAINTAINER itswcg

ARG REQUIREMENT_CONFIG=production
ENV PYTHONUNBUFFERED 1

ADD requirements /requirements

RUN pip install --no-cache-dir -r /requirements/${REQUIREMENT_CONFIG}.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm -rf /requirements

ADD . /app
WORKDIR /app