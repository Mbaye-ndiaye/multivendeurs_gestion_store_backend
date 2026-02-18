#!/bin/bash

set -e

source /venv/bin/activate

if [$1 = "gunicorn" ]; then
    exec gunicorn django.wsgi:application -b 0.0.0.0:8000

else
    exec python manage.py runserver 0.0.0.0:8000
fi