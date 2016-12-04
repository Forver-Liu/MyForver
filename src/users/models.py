#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
from django.contrib import admin

from django.db import models


# Create your models here.

class userType(models.Model):
    display = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.display
      
class admins(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    phonenum = models.IntegerField()
    email = models.EmailField()
    loginsIP = models.GenericIPAddressField(default="0.0.0.0",protocol="both",null=True)
    userinfos = models.CharField(max_length=500,default="user")
    usertype = models.ForeignKey("userType")
    regin_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.username

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'phonenum', 'email','loginsIP','regin_time')
    search_fields = ('username', 'email') 
    
#admin.site.register([userType,admins])
admin.site.register(userType)
admin.site.register(admins,AuthorAdmin)