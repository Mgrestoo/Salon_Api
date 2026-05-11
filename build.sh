#!/usr/bin/env bash
# exit immediately if any command fails
set -o errexit

# install all dependencies from requirements.txt
pip install -r requirements.txt

# collect all static files into staticfiles/ folder
# --noinput means don't ask for confirmation
python manage.py collectstatic --noinput

# run all pending migrations
# this creates/updates database tables on every deploy
python manage.py migrate