# base image
FROM python:3.8-slim

# run create.sql on init
RUN apt update
RUN apt install -y cron

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt-get install -y libpq-dev gcc
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["python3", "api.py"]
