#!/usr/bin/env bash



# python manage.py makemigrations
# python manage.py migrate


gunicorn -b :8000 fraternodjango.wsgi:application