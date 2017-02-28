#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import ssl
import time
import string
import random
import socket
import struct
import logging
import hashlib
import urllib2
import urlparse
import datetime
import traceback
import functools
import contextlib
#import MySQLdb
from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import (
    validate_ipv46_address,
    validate_ipv4_address,
    validate_ipv6_address,
)
from enum import Enum
from constants import Const

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return sorted([(getattr(cls,x),x) for x in dir(cls) if x.startswith('STATUS_') or x.startswith('LEVEL_') and not callable(getattr(cls,x))])

def GetFileSize(path):
    return os.path.getsize( path ) if os.path.isfile( path ) else 0

def isStringLike(anobj):
    try: anobj.lower() + anobj + ''
    except: return False
    else: return True

def random_str(num=5, src=string.ascii_letters+string.digits):
    return ''.join(random.sample(src, num))

def safe_cast(val, to_type, default=None):
    try: return to_type(val)
    except: return default

def get_datetime(text, fmt_input=Const.DATETIME_FMT, fmt_output=Const.DATETIME_FMT):
    try: return datetime.datetime.strptime(text, fmt_input).strftime(fmt_output)
    except: return None


if __name__ == '__main__':
    pass
