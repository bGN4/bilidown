# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import urlresolvers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.conf import settings
from .models import *

def home(request):
    return HttpResponseRedirect( urlresolvers.reverse('admin:{}_{}_changelist'.format(BiliRecord._meta.app_label, BiliRecord._meta.model_name)) )

