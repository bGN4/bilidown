#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import datetime

class Const:
    DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
    DATETIME_NUM = '%Y%m%d%H%M%S%f'
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_NAME = os.path.basename(PROJECT_ROOT)
    HO_REDIS_URL = 'redis://:pwd@127.0.0.1:6379/'
    DAMU_DB_NAME = 'danmaku'
    DAMU_DB_USER = 'root'
    DAMU_DB_PASS = 'root'
    DAMU_DB_HOST = '127.0.0.1'
    DAMU_DB_PORT = '3306'
    SITE_DOMAIN  = ''
    SET_IS_DEBUG = True
    SET_IS_DEBUG = False
    IS_TEST_MODE = sys.argv[1:2] == ['test']
    REPAIR_SALT  = ''
    DEBUG_LOGGER = 'django.logdebug'
    SESSION_COOKIE_SECURE   = False #True
    SECURE_PROXY_SSL_HEADER = None  #('HTTP_X_FORWARDED_PROTOCOL', 'https')
    if 'server' not in platform.release().lower(): # for my PC
        SET_IS_DEBUG = True
        SESSION_COOKIE_SECURE = False
        SECURE_PROXY_SSL_HEADER = None
    elif sys.platform == 'darwin':
        pass
    LOG_FILE_WEB = os.path.join(PROJECT_ROOT, 'debug.log')
    LOG_BKG_TASK = os.path.join(PROJECT_ROOT, 'bgcall.log')

