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
  python manage.py lms shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u, _ = User.objects.get_or_create(username='${ADMIN_USERNAME}', defaults={'email': '${ADMIN_EMAIL:-admin@example.com}', 'is_staff': True, 'is_superuser': True}); u.email='${ADMIN_EMAIL:-admin@example.com}'; u.is_staff=True; u.is_superuser=True; u.set_password('${ADMIN_PASSWORD}'); u.save()"
fi

exec "$@"
