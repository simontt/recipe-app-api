FROM python:3.7-alpine
MAINTAINER Simon Tavernier

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# Uses package manager of Alpine to install, no cache to minimize footprint
RUN apk add --update --no-cache postgresql-client
# Virtual adds name for these dependecies to easily remove after pip install
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
# Copy app from local to app directory in Docker image
COPY ./app /app

# Otherwise image runs app from root account - not recommended
RUN adduser -D user
USER user