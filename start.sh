#!/bin/bash

# Iniciar o Nginx
service nginx start
cat /var/log/nginx/error.log
# Iniciar o servidor Django
python3 /app/manage.py runserver 0.0.0.0:8000
