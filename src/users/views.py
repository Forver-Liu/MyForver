#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse

import models,forms
# Create your views here.

userTypeObj = models.userType.objects
adminObj = models.admins.objects
    
def login(request):
    RST = {'stat':1,'forms':'','msg':''}
    
    if request.method == "POST":
        userForm = forms.loginF(request.POST)
        RST['forms'] = userForm
        
        if userForm.is_valid():
            user = userForm.cleaned_data['username']
            pswd = userForm.cleaned_data['password']
        
            try:
                userGet = adminObj.get(username=user,password=pswd)
                RST['stat'] = 0
                RST['msg'] = 'login success'
                request.session['IS_LOGIN'] = {'user':user}
                
                return HttpResponse("logined")
            except Exception,e:
                print e.message
                RST['msg'] = u'用户名或密码错误'
                return render_to_response('login.html',RST)
        else:
            RST['msg'] = userForm.errors.as_data.values()[0][0].messages[0]
            return render_to_response('login.html',RST)
    else:
        RST['forms'] = forms.loginF()
        RST['msg'] = u'请提交正确的用户名和密码'
        return render_to_response('login.html',RST)

    
def addme(request):

    username = "admin"
    password = "admin"
    phonenum = 110
    email = "admin@forver.com"
    userinfo = "superadmin"
    usertype = userTypeObj.get(id=1)
    lastip = "127.0.0.1"
    
    try:
        user = adminObj.create(username=username,
                               password=password,
                               phonenum=phonenum,
                               email=email,
                               userinfos=userinfo,
                               usertype=usertype,
                               loginsIP=lastip)
        return HttpResponse('add admin success')
    except Exception,e:
        return HttpResponse(e.message)