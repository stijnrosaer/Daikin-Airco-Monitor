# base image
FROM postgres:10.4-alpine

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
COPY create_tables.sql /usr/src/create_tables.sql

ADD setup.sh /docker-entrypoint-initdb.d