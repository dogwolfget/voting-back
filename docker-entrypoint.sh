#!/bin/sh
uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput --clear
uv run gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application
