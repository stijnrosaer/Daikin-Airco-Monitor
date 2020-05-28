#!/usr/bin/env bash
psql --username "$POSTGRES_USER" -d airco_db -a -f /usr/src/create_tables.sql
