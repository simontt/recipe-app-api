FROM python:3.7-alpine
MAINTAINER Simon Tavernier

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
# Copy app from local to app directory in Docker image
COPY ./app /app

# Otherwise image runs app from root account - not recommended
RUN adduser -D user
USER user