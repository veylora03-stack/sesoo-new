#!/bin/sh
set -e

# If DB_HOST is set, try running migrations (works standalone or with compose)
if [ -n "$DB_HOST" ]; then
    echo "Running database migrations..."
    until python manage.py migrate --noinput 2>/dev/null; do
      echo "Database unavailable, retrying in 2 seconds..."
      sleep 2
    done
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --access-logfile - \
  --error-logfile -
