CREATE TABLE status
(
    name varchar,
    time timestamp,
    target integer,
    inside integer,
    outside integer,
    heat integer,
    cool integer,
    mode varchar,
    power integer,
    primary key (name, time)

);