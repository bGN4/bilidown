# -*- coding: utf-8 -*- 
import os
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# ########## bGN4's custom settings start ##########
from common.constants import Const
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
LOG=logging.getLogger(Const.DEBUG_LOGGER)

DATETIME_FORMAT = 'Y-m-d H:i:s'
SESSION_COOKIE_SECURE = Const.SESSION_COOKIE_SECURE

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    #'debug_toolbar.panels.profiling.ProfilingPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    #'JQUERY_URL': '/static/grappelli/jquery/jquery-2.1.4.min.js',
    'JQUERY_URL': '/static/suit/js/jquery-1.8.3.min.js',
    'PROFILER_MAX_DEPTH': 100,
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'DanmakuSub',
    'HEADER_DATE_FORMAT': 'Y-m-d',
    'HEADER_TIME_FORMAT': 'H:i, D',
}

# ########## bGN4's custom settings end ############

ROOT_URLCONF = 'DanmakuSub.urls'

DEBUG = Const.SET_IS_DEBUG

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'

# https://docs.djangoproject.com/en/1.7/topics/i18n/
USE_I18N = True

USE_L10N = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

# Classes used to implement DB routing behavior.
DATABASE_ROUTERS = ['DanmakuSub.dbRouters.DBRouter',]

INSTALLED_APPS = [
    'danmaku',
    'adminex',
    'suit',
    'debug_toolbar',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'DanmakuSub.middleware.TrustedHost',
    'DanmakuSub.middleware.LogRequest',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # List of callables that know how to import templates from various sources.
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eb499c9e-4f59-4004-92d0-816e257479db'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

# URL prefix for static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

WSGI_APPLICATION = 'DanmakuSub.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s #%(levelname).1s -> %(message)s'
        },
        'standard': {
            'format': '%(asctime)s #%(levelname).1s %(process)5d/%(threadName).1s.%(thread)-5d [%(filename)13s:%(lineno)04d] %(name)-15s -> %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'bGN4_custom': {
            '()': 'DanmakuSub.logfilters.bGN4Filter',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level': 'DEBUG',
            'filters': ['bGN4_custom'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': Const.LOG_FILE_WEB,
            'maxBytes': 500*1024*1024,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',#'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default'],#, 'console'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

