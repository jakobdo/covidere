#!/bin/bash

python manage.py makemigrations --merge
python manage.py migrate --noinput

gunicorn shoplokalt.wsgi:application \
    --name shoplokalt \
    --bind 0.0.0.0:8000 \
    --timeout 600 \
    --workers 4 \
    --log-level=info \
    --reload