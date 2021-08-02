#!/bin/bash
export DJANGO_SETTINGS=$DJANGO_SETTINGS_MODULE
export DEFAULT_BIND=0.0.0.0:$PUBLISHED_PORT
export DEFAULT_WORKERS=6
python app/manage.py makemigrations --no-input
python app/manage.py migrate
python app/manage.py collectstatic --no-input
service nginx start
gunicorn app.wsgi --env DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS}" --bind "${DEFAULT_BIND}" --workers=${DEFAULT_WORKERS} --log-level debug --chdir ./app

