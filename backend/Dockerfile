FROM ubuntu:18.04

# install python 3.7.10 (or newer)
RUN apt update
RUN apt install --no-install-recommends -y build-essential software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install --no-install-recommends -y python3.7
RUN apt install python3.7-dev -y
RUN apt install python3.7-distutils -y
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Register the version in alternatives (and set higher priority to 3.7)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2

RUN apt update && apt install python3-pip -y

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
