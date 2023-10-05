FROM python:latest

RUN mkdir /root/src
WORKDIR /root/src
COPY . .

RUN pip install flask requests flask_restx

ENTRYPOINT python -u main.py