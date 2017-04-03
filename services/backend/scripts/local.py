# coding: utf-8

import environ
from .common import *

env = environ.Env()
DEBUG = env('DJANGO_DEBUG', cast=bool, default=False)
PUBLIC_REGISTER_ENABLED = env(
    'TAIGA_PUBLIC_REGISTER_ENABLED', cast=bool, default=True
)

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', cast=list, default=['*'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DJANGO_DB_NAME'),
        'USER': env('DJANGO_DB_USER'),
        'PASSWORD': env('DJANGO_DB_PASSWORD'),
        'HOST': 'postgresql',
        'PORT': '',
    }
}

TAIGA_HOSTNAME = env('TAIGA_HOSTNAME', default='localhost')
REDIS_URL = env('REDIS_URL', default='redis://redis:6379')

_HTTP = 'https' if env('TAIGA_SSL', cast=bool, default=False) else 'http'

SITES = {
    "api": {
        "scheme": _HTTP,
        "domain": TAIGA_HOSTNAME,
        "name": "api"
    },
    "front": {
        "scheme": _HTTP,
        "domain": TAIGA_HOSTNAME,
        "name": "front"
    },
}

SITE_ID = "api"

MEDIA_URL = "{}://{}/media/".format(_HTTP, TAIGA_HOSTNAME)
STATIC_URL = "{}://{}/static/".format(_HTTP, TAIGA_HOSTNAME)
MEDIA_ROOT = '/taiga_backend/media'
STATIC_ROOT = '/taiga_backend/static-root'

# Async
BROKER_URL = 'amqp://taiga:taiga@rabbitmq:5672/taiga'
EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
EVENTS_PUSH_BACKEND_OPTIONS = {"url": "amqp://taiga:taiga@rabbitmq:5672/taiga"}

CELERY_ENABLED = env('CELERY', cast=bool, default=True)
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TIMEZONE = 'Europe/Madrid'

# Mail settings
if env('USE_ANYMAIL', cast=bool, default=False):
    INSTALLED_APPS += ['anymail']
    ANYMAIL = {
        "MAILGUN_API_KEY": env('ANYMAIL_MAILGUN_API_KEY'),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
    DEFAULT_FROM_EMAIL = "Taiga <{}>".format(env('DJANGO_DEFAULT_FROM_EMAIL'))

# Cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake"
#     }
# }

# *************** SMTP
if env('SMTP', cast=bool, default=False):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

if env('LDAP', cast=bool, default=False):
    INSTALLED_APPS += ["taiga_contrib_ldap_auth"]

    LDAP_SERVER = env('LDAP_SERVER')
    LDAP_PORT = env('LDAP_PORT', cast=int, default=636)

    # Full DN of the service account use to connect to LDAP server and search for login user's account entry
    # If LDAP_BIND_DN is not specified, or is blank, then an anonymous bind is attempated
    LDAP_BIND_DN = env('LDAP_BIND_DN')
    LDAP_BIND_PASSWORD = env('LDAP_BIND_PASSWORD')
    # Starting point within LDAP structure to search for login user
    LDAP_SEARCH_BASE = env('LDAP_SEARCH_BASE')
    # LDAP property used for searching, ie. login username needs to match value in sAMAccountName property in LDAP
    LDAP_SEARCH_PROPERTY = env('LDAP_SEARCH_PROPERTY', default='uid') # 'posixAccount'
    LDAP_SEARCH_SUFFIX = env('LDAP_SEARCH_SUFFIX', default='')

    # Names of LDAP properties on user account to get email and full name
    LDAP_EMAIL_PROPERTY = env('LDAP_EMAIL_PROPERTY', default='mail')
    LDAP_FULL_NAME_PROPERTY = env('LDAP_FULL_NAME_PROPERTY', default='cn')
