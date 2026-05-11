#!/usr/bin/env bash
# exit immediately if any command fails
set -o errexit

# install all dependencies from requirements.txt
pip install -r requirements.txt

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

# collect all static files into staticfiles/ folder
# --noinput means don't ask for confirmation
python manage.py collectstatic --noinput
