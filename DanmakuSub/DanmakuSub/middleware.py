# -*- coding: utf-8 -*-

import os
import time
import json
import random
import urllib
import logging
import traceback
from django.http import HttpResponseForbidden
from django.conf import settings
from common.constants import Const
#from common.utils import safe_cast

logger = logging.getLogger('django.request')

class TrustedHost(object):

    def process_request(self, request):
        remote_addr = request.META['HTTP_X_REAL_IP'] if request.META.has_key('HTTP_X_REAL_IP') else request.META.get('REMOTE_ADDR', '')

class LogRequest(object):
    debug_stime = None

    def process_request(self, request):
        self.debug_stime = time.time()
        #logger.debug('{0} {1} {2} {3} {4}'.format(request.META.get('REMOTE_ADDR', '-'), 
        #                                          request.method,
        #                                          request.get_full_path(), 
        #                                          request.META.get('HTTP_X_REAL_IP', '-'), 
        #                                          request.META.get('HTTP_X_FORWARDED_FOR', '-')))

    def process_response(self, request, response):
        try: response._headers.pop('content-disposition')
        except: pass
        try:
            logger.debug('{} {} {} {} {} {} {} {} {} {}ms'.format(
                request.META.get('REMOTE_ADDR', '-'),
                getattr(request, 'user', '-'),
                response.status_code,
                request.method,
                request.get_full_path(),
                request.META.get('HTTP_X_REAL_IP', '-'),
                request.META.get('HTTP_X_FORWARDED_FOR', '-'),
                getattr(request, 'test1', '-'),
                getattr(request, 'test2', '-'),
                int(1000*(time.time()-self.debug_stime)))
            )
        except Exception as e:
            logger.warn( e )
        return response


