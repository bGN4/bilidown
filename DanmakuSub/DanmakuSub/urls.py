from django.conf.urls import patterns, include, url
from django.conf import settings
from common.constants import Const
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$',                      'danmaku.views.home',           name='home'),
    #url(r'^contact$',              'app.views.contact',            name='contact'),
    #url(r'^about',                 'app.views.about',              name='about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
