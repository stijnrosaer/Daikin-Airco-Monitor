# base image
FROM python:3.8-slim

# run create.sql on init
RUN apt update
RUN apt install -y cron

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python3", "api.py"]
