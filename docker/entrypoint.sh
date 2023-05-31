#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST 5432; do
      sleep 0.1
    done


    echo "PostgreSQL started"
fi

exec uvicorn src.main:app --host 0.0.0.0 --port 8080

exec "$@"