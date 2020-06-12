FROM python:3.7-alpine
MAINTAINER Simon Tavernier

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# Uses package manager of Alpine to install, no cache to minimize footprint
# jpeg-dev is Linux package that's needed to pip install Pillow;
# look at PyPI page of Pillow to see these dependencies
RUN apk add --update --no-cache postgresql-client jpeg-dev
# Virtual adds name for these dependecies to easily remove after pip install
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
# Copy app from local to app directory in Docker image
COPY ./app /app

# Files that may need to be shared with other containters in vol
# media contains files uploaded by user, static contains js and css
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# Otherwise image runs app from root account - not recommended
RUN adduser -D user
# Give user permission to the files BEFORE switching to user;
# user can not give permission for itself
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user