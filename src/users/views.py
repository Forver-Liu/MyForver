#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse

import json

import models,forms
# Create your views here.

userTypeObj = models.userType.objects
adminObj = models.admins.objects
 
def checklogin(func):
    def _desc(request,*args,**kwargs):
        if not request.session.get('IS_LOGIN'):
            return redirect('/hostM/login/')
        else:
            return func(request,*args,**kwargs)
    return _desc

   
def login(request):
    RST = {'stat':1,'forms':'','msg':''}
    
    if request.method == "POST":
        postObj = request.POST
        userForm = forms.loginF(postObj)
        RST['forms'] = userForm
        
        if userForm.is_valid():
            user = userForm.cleaned_data['username']
            pswd = userForm.cleaned_data['password']
        
            try:
                userGet = adminObj.get(username=user,password=pswd)
                RST['stat'] = 0
                RST['msg'] = 'login success'
                request.session['IS_LOGIN'] = {'user':user}
                
                #return HttpResponse("logined")
                return redirect('/users/user_index/')
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


def logout(request):
    login_dic = request.session.get('IS_LOGIN',None)
    if login_dic:
        print login_dic
        del request.session['IS_LOGIN']
    return redirect('/users/login/')

def user_index(request):
    RST={'stat':0,'data':'','form':'','msg':''}
    registForm = forms.regist()
    RST['form'] = registForm
    
    RST['data'] = adminObj.all()
    print RST
    #return HttpResponse(json.dumps(RST))
    return render_to_response('index.html',RST)
    
def regist(request):
    RST = {'stat':0,'msg':'','form':'','usertype':'',}
    RST['usertype'] = userTypeObj.all()
    
    if request.method == "POST":
        form = forms.registF(request.POST)
        print form
        if form.is_valid():
            print "1111"
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            infos = form.cleaned_data['infos']
            usertype = userTypeObj.get(id=int(request.POST['usertype']))
            lastip = request.META['REMOTE_ADDR']
    
            try:
                user = adminObj.create(username=username,
                                       password=password,
                                       phonenum=phone,
                                       email=email,
                                       userinfos=infos,
                                       usertype=usertype,
                                       loginsIP=lastip)
                return HttpResponse('add admin success')
            except Exception,e:
                return HttpResponse(e.message)
        else:
            print "1112222"
            RST['msg'] = form.errors#.as_data.values()[0][0].messages[0]
            #RST['msg'] = "error formate"
            RST['form'] = form
            return render_to_response('regist.html',RST)
    else:
        print "222222"
        #RST['msg'] = "POST request need"
        RST['form'] = forms.registF()
        return render_to_response('regist.html',RST)