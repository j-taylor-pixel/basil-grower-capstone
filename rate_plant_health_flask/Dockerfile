# syntax=docker/dockerfile:1

FROM ubuntu:latest

USER root

RUN apt-get update
RUN apt-get install -y python3.11
RUN apt install python3-pip -y

WORKDIR /

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt requirements.txt
RUN pip3 install ultralytics
RUN pip3 install flask
RUN pip3 install opencv-python-headless

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]