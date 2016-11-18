FROM tailordev/pandas:0.19.0
MAINTAINER Adrienn Szabo "ador@protonmail.com"

## Notes
## -----
## This is mainly for development and testing purposes.
## How to  build: docker build -t "yo-port-2016" .
## How to run:  docker run -u yoda -t -i yo-port-2016 /bin/bash


# use bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && apt-get install -yq unzip wget git ssh nano curl less

RUN pip install --upgrade pip
RUN pip install matplotlib
RUN pip install seaborn
RUN pip install scikit-learn
RUN pip install scipy
RUN pip install pytest

# create non-root but sudoer user "yoda"
RUN useradd -ms /bin/bash yoda
ENV HOME /home/yoda
RUN adduser yoda sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

