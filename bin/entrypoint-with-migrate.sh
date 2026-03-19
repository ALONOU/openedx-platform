#!/usr/bin/env bash
set -e
cd /openedx/edx-platform

# Eviter les migrations concurrentes: uniquement dans le conteneur LMS
if [[ "${RUN_MIGRATIONS:-0}" == "1" ]]; then
  # MySQL peut accepter le healthcheck avant d'être prêt pour de longues migrations
  _max="${MIGRATE_RETRY_MAX:-12}"
  _n=0
  while [[ "${_n}" -lt "${_max}" ]]; do
    if python manage.py lms migrate --noinput && python manage.py cms migrate --noinput; then
      break
    fi
    _n=$((_n + 1))
    echo "[entrypoint] migrate failed (attempt ${_n}/${_max}), retry in ${MIGRATE_RETRY_SLEEP:-5}s..."
    sleep "${MIGRATE_RETRY_SLEEP:-5}"
  done
  if [[ "${_n}" -ge "${_max}" ]]; then
    echo "[entrypoint] migrate gave up after ${_max} attempts"
    exit 1
  fi

  # OAuth Studio -> LMS: créer/metre à jour le client DOT pour éviter client_id=None dans Studio
  STUDIO_OAUTH_CLIENT_ID="${SOCIAL_AUTH_EDX_OAUTH2_KEY:-studio-sso}"
  STUDIO_OAUTH_CLIENT_SECRET="${SOCIAL_AUTH_EDX_OAUTH2_SECRET:-studio-sso-secret}"
  STUDIO_REDIRECT_URI="${CMS_ROOT_URL%/}/complete/edx-oauth2/"
  python manage.py lms manage_user studio_worker "${ADMIN_EMAIL:-admin@example.com}" --unusable-password || true
  python manage.py lms create_dot_application studio-sso studio_worker \
    --grant-type authorization-code \
    --skip-authorization \
    --redirect-uris "${STUDIO_REDIRECT_URI}" \
    --scopes "user_id" \
    --client-id "${STUDIO_OAUTH_CLIENT_ID}" \
    --client-secret "${STUDIO_OAUTH_CLIENT_SECRET}" \
    --update || true
fi

# Création superuser au 1er démarrage si les variables sont définies
if [[ "${RUN_MIGRATIONS:-0}" == "1" && -n "${ADMIN_USERNAME:-}" && -n "${ADMIN_PASSWORD:-}" ]]; then
  # Do not interpolate secrets in python code to avoid quoting crashes.
  python manage.py lms shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('ADMIN_USERNAME'); email = os.environ.get('ADMIN_EMAIL', 'admin@example.com'); password = os.environ.get('ADMIN_PASSWORD'); u, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); u.email = email; u.is_staff = True; u.is_superuser = True; u.set_password(password); u.save()" || true
fi

exec "$@"
