#!/bin/bash

# Set the PORT environment variable if not already set
: ${PORT:=8000}

# Wait for database to be ready
echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h "db" --silent; do
    sleep 1
done

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (optional, uncomment if needed)
# python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT 
