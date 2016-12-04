#!/usr/bin/env python
#coding:utf-8

from django import forms

class loginF(forms.Form):
    username = forms.CharField(max_length=150,error_messages={'required':u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(),error_messages={'required':u'密码不能为空'})

class registF(forms.Form):
    username = forms.CharField(label="用户名",max_length=100,required=True,error_messages={'required':u'用户名不能为空'})
    password = forms.CharField(label="密     码",widget=forms.PasswordInput(),required=True,error_messages={'required':u'密码不能为空'})
    email = forms.EmailField(label="邮箱",required=True,error_messages={'required':u'又将不鞥为空','invalid':u'内容无效，邮箱格式错误'})
    