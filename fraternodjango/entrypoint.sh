#!/usr/bin/env bash

python manage.py collectstatic --noinput

python manage.py spectacular --color --file schema.yml

python manage.py makemigrations
python manage.py migrate
gunicorn -b :8000 appname.wsgi