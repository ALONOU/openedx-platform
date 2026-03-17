# -*- coding: utf-8 -*-
"""
Custom LMS settings for Docker/Coolify.

On part de la config complète Open edX (lms/envs/common)
et on override seulement l’infra (MySQL, Mongo, Redis, langue…).
"""

import os

from openedx.envs.common import *  # noqa

# ============================================================================
# BASE / SERVICE
# ============================================================================

SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', 'lms')

# ============================================================================
# DATABASE (MySQL dans Docker)
# ============================================================================

DATABASES['default'].update({
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ.get('MYSQL_DATABASE', DATABASES['default'].get('NAME', 'openedx')),
    'USER': os.environ.get('MYSQL_USER', DATABASES['default'].get('USER', 'openedx')),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', DATABASES['default'].get('PASSWORD')),
    'HOST': os.environ.get('MYSQL_HOST', 'mysql'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
})

if 'OPTIONS' in DATABASES['default']:
    DATABASES['default']['OPTIONS'].setdefault('charset', 'utf8mb4')

# ============================================================================
# MONGODB (modulestore)
# ============================================================================

CONTENTSTORE['DOC_STORE_CONFIG'].update({
    'host': os.environ.get('MONGO_HOST', 'mongodb'),
    'port': int(os.environ.get('MONGO_PORT', '27017')),
    'db': os.environ.get('MONGO_DATABASE', CONTENTSTORE['DOC_STORE_CONFIG'].get('db', 'openedx')),
    'user': os.environ.get('MONGO_USER', CONTENTSTORE['DOC_STORE_CONFIG'].get('user')),
    'password': os.environ.get('MONGO_PASSWORD', CONTENTSTORE['DOC_STORE_CONFIG'].get('password')),
})

MODULESTORE['default']['DOC_STORE_CONFIG'] = CONTENTSTORE['DOC_STORE_CONFIG']

# ============================================================================
# REDIS (cache + sessions + Celery broker)
# ============================================================================

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))

if 'default' in CACHES:
    CACHES['default']['LOCATION'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/1')

# ============================================================================
# LOCALISATION / LANGUE
# ============================================================================

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', LANGUAGE_CODE)
TIME_ZONE = os.environ.get('TIME_ZONE', TIME_ZONE)

