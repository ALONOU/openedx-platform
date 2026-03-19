# -*- coding: utf-8 -*-
"""
Production Django settings for Open edX CMS/Studio (Native Setup)
"""

import os
from .common import *
from openedx.core.lib.derived import derive_settings

# ============================================================================
# PRODUCTION SETTINGS
# ============================================================================

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# ============================================================================
# INFRA (Docker/Coolify) overrides
# ============================================================================

# MySQL (service docker: mysql)
DATABASES['default'].update({
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ.get('MYSQL_DATABASE', DATABASES['default'].get('NAME')),
    'USER': os.environ.get('MYSQL_USER', DATABASES['default'].get('USER')),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', DATABASES['default'].get('PASSWORD')),
    'HOST': os.environ.get('MYSQL_HOST', 'mysql'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
})
if 'OPTIONS' in DATABASES['default']:
    DATABASES['default']['OPTIONS'].setdefault('charset', 'utf8mb4')

# Mongo (service docker: mongodb)
CONTENTSTORE['DOC_STORE_CONFIG'].update({
    'host': os.environ.get('MONGO_HOST', 'mongodb'),
    'port': int(os.environ.get('MONGO_PORT', '27017')),
    'db': os.environ.get('MONGO_DATABASE', CONTENTSTORE['DOC_STORE_CONFIG'].get('db')),
    'user': os.environ.get('MONGO_USER', CONTENTSTORE['DOC_STORE_CONFIG'].get('user')),
    'password': os.environ.get('MONGO_PASSWORD', CONTENTSTORE['DOC_STORE_CONFIG'].get('password')),
    'authsource': os.environ.get('MONGO_AUTH_SOURCE', 'admin'),
})
MODULESTORE['default']['DOC_STORE_CONFIG'] = CONTENTSTORE['DOC_STORE_CONFIG']

# Redis (service docker: redis)
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
if 'default' in CACHES:
    CACHES['default']['LOCATION'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/1')

# Locale
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', LANGUAGE_CODE)
TIME_ZONE = os.environ.get('TIME_ZONE', TIME_ZONE)

# Fichiers média (volume data généralement writable en conteneur)
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/openedx/data/media')
try:
    os.makedirs(MEDIA_ROOT, exist_ok=True)
except OSError:
    # Ne pas faire échouer l'import Django si le volume n'est pas encore writable (uid/gid)
    pass

# URLs (Open edX upstream laisse LMS_ROOT_URL=None → requis pour les Derived())
LMS_ROOT_URL = os.environ.get('LMS_ROOT_URL') or 'http://localhost:8000'
CMS_ROOT_URL = os.environ.get('CMS_ROOT_URL') or 'http://localhost:8001'
# Studio authoring MFE URL (requis par Open edX Studio header)
COURSE_AUTHORING_MICROFRONTEND_URL = (
    os.environ.get('COURSE_AUTHORING_MICROFRONTEND_URL')
    or f"{CMS_ROOT_URL.rstrip('/')}/authoring"
)
# OAuth Studio <-> LMS (évite /login/edx-oauth2/None/...)
def _env_not_none(name: str, default: str) -> str:
    """
    Normalise les variables d'env qui peuvent arriver avec des valeurs littérales
    type 'None'/'null' depuis certaines UIs (Coolify, etc.).
    """
    val = os.environ.get(name)
    if val is None:
        return default
    if isinstance(val, str) and val.strip().lower() in {"", "none", "null"}:
        return default
    return val

SOCIAL_AUTH_EDX_OAUTH2_KEY = _env_not_none('SOCIAL_AUTH_EDX_OAUTH2_KEY', 'studio-sso')
SOCIAL_AUTH_EDX_OAUTH2_SECRET = _env_not_none('SOCIAL_AUTH_EDX_OAUTH2_SECRET', 'studio-sso-secret')
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT', LMS_ROOT_URL)
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = os.environ.get('SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT', LMS_ROOT_URL)

# Cache: forcer Redis (évite memcached + adresse mal formée type "6379/0")
_redis_cache_location = os.environ.get('DJANGO_CACHE_LOCATION') or f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': _redis_cache_location,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        'TIMEOUT': int(os.environ.get('CACHE_TIMEOUT', '300')),
    }
}

# Celery: Open edX lit surtout BROKER_URL
BROKER_URL = os.environ.get('BROKER_URL') or CELERY_BROKER_URL

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# Par défaut: stdout uniquement (Coolify/Docker). RotatingFileHandler sur volume peut
# provoquer PermissionError au boot → crash-loop si /openedx/data/logs n'est pas writable.
_use_file_logging = os.environ.get('DJANGO_USE_FILE_LOGGING', '0') == '1'
_log_handlers = ['console']
_handlers = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'standard',
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
}
if _use_file_logging:
    try:
        os.makedirs('/openedx/data/logs', exist_ok=True)
        test_path = '/openedx/data/logs/.write_test'
        with open(test_path, 'a'):
            pass
        os.remove(test_path)
        _handlers['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/openedx/data/logs/cms.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'INFO',
        }
        _log_handlers = ['console', 'file']
    except OSError:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s'
        },
    },
    'handlers': _handlers,
    'loggers': {
        'django': {
            'handlers': list(_log_handlers),
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': list(_log_handlers),
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'celery': {
            'handlers': list(_log_handlers),
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': list(_log_handlers),
            'level': 'INFO',
        },
    },
}

# ============================================================================
# SECURITY SETTINGS (Production)
# ============================================================================

# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Template caching
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Finalise les settings "Derived(...)" d'Open edX (ex: LOCALE_PATHS doit être une liste)
derive_settings(__name__)
