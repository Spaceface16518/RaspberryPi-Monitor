FROM python:3.8-slim-buster

MAINTAINER Amrit Rathie

WORKDIR /usr/src/app

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD [ "python", "./app.py" ]