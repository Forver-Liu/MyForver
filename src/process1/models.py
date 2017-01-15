#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
from django.contrib import admin

from django.db import models


# Create your models here.

class UserType(models.Model):
    display = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.display
    
class Admin(models.Model):
    username = models.CharField(max_length=350)
    password = models.CharField(max_length=350)
    email = models.EmailField()
    user_type = models.ForeignKey("UserType")
    
    def __unicode__(self):
        return self.username
    
class Chat(models.Model):
    contents = models.CharField(max_length=500)
    user = models.ForeignKey("Admin")
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.contents
    
class NewsType(models.Model):
    display = models.CharField(max_length=350)
    
    def __unicode__(self):
        return self.display
    
class News(models.Model):
    title = models.CharField(max_length=1050)
    summary = models.CharField(max_length=500)
    url = models.URLField()
    favor_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    news_type = models.ForeignKey("NewsType")
    user = models.ForeignKey("Admin")
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
class Reply(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey("Admin")
    news = models.ForeignKey("News")
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.content
    

admin.site.register([UserType,Admin,Chat,NewsType,News,Reply])