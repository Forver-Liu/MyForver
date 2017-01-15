#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年11月26日

@author: Forver
'''

from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    #url(r'^adddatas/',views.adddatas),
    
    url(r'^index/',views.index),
    url(r'^addfavor/',views.addfavor),
    url(r'^getreply/',views.getreply),
    url(r'^submitreply/',views.submitreply),
    
    url(r'^login/',views.login),
    
    url(r'^chat/',views.chat),
    url(r'^subchat/',views.subchat),
    url(r'^getchats/',views.getchats),
    url(r'^getchats2/',views.getchats2),
    
    
]