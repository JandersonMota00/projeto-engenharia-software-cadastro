
pip freeze

gunicorn fraternodjango.wsgi:application --bind 0.0.0.0:8000