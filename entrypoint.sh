#!/bin/sh
set -e

# The /media volume is created by Docker as root:root on first run,
# so it must be re-owned to appuser before that user can write to it.
chown -R appuser:appuser /media

gosu appuser python manage.py migrate --noinput
gosu appuser python manage.py collectstatic --noinput

exec gosu appuser gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile -
