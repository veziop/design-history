FROM python:3.8-alpine
MAINTAINER Valentin Piombo valenp97@gmail.com

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /project
WORKDIR /project
COPY ./project /project

RUN adduser -D user
USER user