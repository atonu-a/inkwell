#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate


python manage.py shell -c "from django.contrib.auth import get_user_model; import os; User = get_user_model(); u, created = User.objects.get_or_create(username='AtonuRoy'); u.set_password(os.environ.get('DJANGO_SUPERUSER_PASSWORD')); u.is_superuser=True; u.is_staff=True; u.save()"

