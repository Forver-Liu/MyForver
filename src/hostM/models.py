#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    userTypeID = models.ForeignKey('UserType',default=1)
    
admin.site.register(AdminUser)

class UserType(models.Model):
    TypeName = models.CharField(max_length=50)