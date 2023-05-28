FROM python:3.11.3-slim-buster

ENV PYTHONINBUFFERED=1

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install --no-install-recommends binutils libproj-dev gdal-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django-gis-api

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .
