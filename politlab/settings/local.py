# -*- coding: utf-8 -*-
from politlab.settings.settings import *

SITE_ID = 1 
SITE_URL = 'http://127.0.0.1:8000'
LOGOUT_REDIRECT_URL = SITE_URL
LOGIN_REDIRECT_URL = SITE_URL

SECRET_KEY = '&=!!k8)tn)c!%u%r$u^xau3wq4g(idf%&_zn&!gv^%g(-1#+--'

DEBUG = True

SESSION_EXPIRE_AT_BROWSER_CLOSE=True

ADMINS = (
    ('Josir', 'josircg@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'politlab',
        'USER': 'politlab',
        'PASSWORD': 'politlab',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    },
    'tse': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tse',
        'USER': 'politlab',
        'PASSWORD': 'politlab',
        'HOST': '',
        'PORT': '',
    }
}


ALLOWED_HOSTS = ['127.0.0.1', ]
SITE_HOST = 'http://127.0.0.1'

EMAIL_SUBJECT_PREFIX = u'[PolitLab] Errors and Warnings'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'user@server'
