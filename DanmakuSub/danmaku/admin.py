# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.utils import timezone
from django.core import urlresolvers
from django.contrib import admin
from django.db import models
from django import forms
from .models import *


@admin.register(BiliComment)
class BiliCommentAdmin(admin.ModelAdmin):
    list_display = ('id', '_x_url', '_x_cid', 'status', 'count', 'expire', 'ntime', 'atime')
    list_filter  = ('status', 'expire', 'ntime', 'atime')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style':'width:80%; margin-right:10px;'})},
    }

    def _x_url(self, obj):
        return '<a href="{url}" target="_blank">{text}</a>'.format(url='http://www.bilibili.com/video/av%s/index_%s.html'%(obj.aid,obj.pid), text=obj)
    _x_url.admin_order_field = 'aid'
    _x_url.short_description = 'URL'
    _x_url.allow_tags = True

    def _x_cid(self, obj):
        return '<a href="{url}" target="_blank">{text}</a>'.format(url='http://comment.bilibili.com/%s.xml'%obj.cid, text=obj.cid)
    _x_url.admin_order_field = 'cid'
    _x_url.short_description = 'cid'
    _x_url.allow_tags = True


@admin.register(BiliRecord)
class BiliRecordAdmin(admin.ModelAdmin):
    list_display = ('url', 'status', 'atime')
    exclude = ('status', 'comment', 'user', 'deleted')
    list_filter  = ('status', 'atime')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style':'width:80%; margin-right:10px;'})},
    }

    class Media:
        js = ()

    def delete_model(self, request, obj):
        if obj.deleted != 1:
            obj.deleted = 1
            obj.save()

