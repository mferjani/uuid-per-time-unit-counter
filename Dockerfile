FROM python:3.8-buster

RUN apt update && apt install -y nano

# Copy source to container
RUN mkdir -p /usr/app/src
RUN mkdir -p /usr/app/bin


# Copy source code
COPY ./app/src /usr/app/src
COPY ./app/bin /usr/app/bin

COPY requirements.txt /usr/app

WORKDIR /usr/app

RUN pip install -r /usr/app/requirements.txt
