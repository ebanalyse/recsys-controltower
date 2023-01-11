FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /backend
RUN apt-get update && apt-get install -y \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /backend

COPY requirements.txt /backend/requirements.txt
RUN pip install -r /backend/requirements.txt

COPY src /backend
WORKDIR /backend

RUN python manage.py collectstatic --noinput

# Dont destroy build cache
ARG GIT_HASH=NA
ENV GIT_HASH ${GIT_HASH}

ENTRYPOINT [ "dumb-init", "--" ]
