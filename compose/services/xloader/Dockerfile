FROM alpine:3.14

ARG XLOADER_VERSION=${XLOADER_VERSION}

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone
ENV GIT_URL=https://github.com/ckan/datapusher.git
ENV JOB_CONFIG=${APP_DIR}/datapusher_settings.py

WORKDIR ${APP_DIR}

# Set up timezone
RUN apk add --no-cache tzdata
RUN echo ${TZ} > /etc/timezone

RUN apk add --no-cache \
    bash \ 
    curl \
    python3 \
    py3-pip \
    py3-wheel \
    libffi-dev \
    libmagic \
    libressl-dev \
    libxslt \
    uwsgi \
    uwsgi-http \
    uwsgi-corerouter \
    uwsgi-python \
    # Temporary packages to build DataPusher requirements
    && apk add --no-cache --virtual .build-deps \
    gcc \
    git \
    musl-dev \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    cargo \
    wget

# install xloader
RUN pip3 install -e 'git+https://github.com/ckan/ckanext-xloader.git@master#egg=ckanext-xloader' && \ 
   pip3 install -r ${APP_DIR}/src/ckanext-xloader/dev-requirements.txt && \
   pip3 install -U requests[security]



CMD ["bash", "-c", "ckan -c /srv/app/ckan.ini jobs worker"]