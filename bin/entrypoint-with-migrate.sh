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
  python manage.py lms createsuperuser \
    --noinput \
    --username "${ADMIN_USERNAME}" \
    --email "${ADMIN_EMAIL:-admin@example.com}" \
    || true
  python manage.py lms shell -c "from django.contrib.auth import get_user_model; u = get_user_model().objects.filter(username='${ADMIN_USERNAME}').first(); u and (u.set_password('${ADMIN_PASSWORD}') or u.save())" || true
fi

exec "$@"
