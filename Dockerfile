FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y

RUN apt-get install -y \
    python3-pip \
    python3-setuptools \
    i2c-tools \
    libgpiod-dev \
    python3-libgpiod \
    fonts-dejavu \
    python3-pil \
    vim-tiny

RUN rm --force --recursive /var/lib/apt/lists/*
RUN rm --force --recursive /usr/share/doc
RUN rm --force --recursive /usr/share/man
RUN apt clean

# Allow installing stuff to system Python.
RUN rm --force /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade RPi.GPIO
RUN pip3 install --upgrade adafruit-blinka
RUN pip3 install adafruit-circuitpython-epd

COPY assets/meteocons.ttf /usr/share/fonts/truetype/meteocon/meteocons.ttf

WORKDIR /root/workdir

COPY src/ /root/workdir/

ENTRYPOINT [ "/usr/bin/bash" ]