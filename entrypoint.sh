#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input


# gunicorn near_server.wsgi:application --bind 0.0.0.0:8000
# gunicorn near_server.asgi:application -k uvicorn.workers.UvicornWorker

gunicorn near_server.asgi:application --forwarded-allow-ips='*' --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker
# gunicorn near_server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80