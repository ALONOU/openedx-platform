#!/usr/bin/env bash
set -e
cd /openedx/edx-platform

# Eviter les migrations concurrentes: uniquement dans le conteneur LMS
if [[ "${RUN_MIGRATIONS:-0}" == "1" ]]; then
  python manage.py lms migrate --noinput
  python manage.py cms migrate --noinput
fi

# Création superuser au 1er démarrage si les variables sont définies
if [[ "${RUN_MIGRATIONS:-0}" == "1" && -n "${ADMIN_USERNAME:-}" && -n "${ADMIN_PASSWORD:-}" ]]; then
  # Do not interpolate secrets in python code to avoid quoting crashes.
  python manage.py lms shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('ADMIN_USERNAME'); email = os.environ.get('ADMIN_EMAIL', 'admin@example.com'); password = os.environ.get('ADMIN_PASSWORD'); u, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); u.email = email; u.is_staff = True; u.is_superuser = True; u.set_password(password); u.save()" || true
fi

exec "$@"
