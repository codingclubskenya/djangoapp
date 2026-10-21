#!/bin/bash
#
# Deploy script for Django API (djangoapp repo)
# Run on server: bash deploy.sh
#
set -e

APP_DIR=/home/devops/deheus-api-django
GIT_REPO=https://github.com/codingclubskenya/djangoapp.git
BRANCH=joe

echo "=== Pulling latest code ==="
cd $APP_DIR
git pull origin $BRANCH

echo "=== Installing dependencies ==="
$APP_DIR/venv/bin/pip install -r requirements.txt

echo "=== Collecting static files ==="
$APP_DIR/venv/bin/python manage.py collectstatic --noinput

echo "=== Running migrations ==="
$APP_DIR/venv/bin/python manage.py migrate --noinput

echo "=== Restarting Gunicorn ==="
sudo systemctl restart gunicorn

echo "=== Deploy complete ==="
