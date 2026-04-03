# #!/bin/bash

# set -e



# python manage.py migrate
# python manage.py collectstatic --noinput

# gunicorn backend.wsgi:application --bind 0.0.0.0:8000

# if [ "$1" = "gunicorn" ]; then
#     exec gunicorn backend.wsgi:application -b 0.0.0.0:8000

# else
#     exec python manage.py runserver 0.0.0.0:8000
# fi


#!/bin/bash

set -e

echo "🚀 Applying migrations..."
python manage.py migrate

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔥 Starting server..."

if [ "$1" = "gunicorn" ]; then
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
else
    exec python manage.py runserver 0.0.0.0:8000
fi