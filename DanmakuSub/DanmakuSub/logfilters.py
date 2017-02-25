# -*- coding: utf-8 -*-

import re
import logging

class bGN4Filter(logging.Filter):

    _re_select_progress = re.compile(r'SELECT `auth_user`')

    def filter(self, record):
        if record.levelno<=10:
            if record.name=='django.db.backends':
                msg = record.getMessage()
                if ('SET SQL_AUTO_IS_NULL = 0; args='       in msg or
                    'SELECT `django_'                       in msg):
                    return False
                elif self._re_select_progress.search(msg):
                    return False
            elif record.name=='django.request':
                msg = record.getMessage()
                if ('200 GET /admin/jsi18n'                 in msg or
                    '200 GET /admin/jsi18n'                 in msg):
                    return False
        return True

