#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse, redirect
import myforms,models
from django.utils.safestring import mark_safe
from django.template.context import RequestContext
# Create your views here.

def adduser(request):
    #ULR:/hostM/adduser/?user=admin&passwd=admin
    print request
    name = request.GET['user',None]
    passwd = request.GET['passwd',None]
    
    datas = models.AdminUser.objects
    print "All datas:%s"%datas.all()
    
    if datas.filter(username=name):
        print "user:%s was alward in admin users"%name
    else:
        datas.create(username=name,password=passwd)
        print "add user\(%s\) successed"%name
    
    ### delete user
    #datas.filter(username=name).delete()
    return HttpResponse('ok')
    
def addUserType(request):
    datas = models.UserType.objects
    datas.create(TypeName=u'超级管理员')
    datas.create(TypeName=u'数据库管理员')
    datas.create(TypeName=u'主机管理员')
    datas.create(TypeName=u'查看')
    datas.create(TypeName=u'主机查看')
    datas.create(TypeName=u'数据库查看')
    
    return HttpResponse('add usertype ok')

#用户登录验证装饰器
def checklogin(func):
    def _desc(request,*args,**kwargs):
        if not request.session.get('IS_LOGIN'):
            return redirect('/hostM/login/')
        else:
            return func(request,*args,**kwargs)
    return _desc

def login(request):
    info=""
    
    if request.method == "POST":

        userForm = myforms.loginF(request.POST)
        if userForm.is_valid():
            print "post data is valid"
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            
            user = models.AdminUser.objects.filter(username__exact=username,password__exact=password)
            if user:
                print user
                print "administrator logined successful"
                request.session['IS_LOGIN'] = {'user':username}
               
                return redirect('/hostM/index/')
            else:
                info = u'用户名或密码错误'
                return render_to_response('login.html',{'UserForms':userForm,'status':info})
        else:
            info=userForm.username['error_messages']
    else:
        userForm = myforms.loginF()
    return render_to_response('login.html',{'UserForms':userForm,'status':info})

def regist(request):
    
    RST = {'RForm':'','msgs':'','usertype':''}
    RST['usertype'] = models.UserType.objects.all()

    if request.method == "POST":
        registForm = myforms.registF(request.POST)
        print registForm
        RST['RForm'] = registForm
        if registForm.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            usertypeID = request.POST['usertype']
            typeObj = models.UserType.objects.get(id=usertypeID)
            
            datas = models.AdminUser.objects
            user = datas.filter(username=username)
            
            if user:
                RST['msgs'] = "User %s is alwardy in"%user
                return render_to_response('regist.html',RST)
            else:
                datas.create(username=username,password=password,email=email,userTypeID=typeObj)
                return HttpResponse('regist success')
        else:
            print registForm.errors()
            First_err = registForm.errors().as_data().values()[0][0].messages[0]
            RST['msgs'] = First_err
            return render_to_response('regist.html',RST)
    else:
        RST['RForm'] = myforms.registF()
        return render_to_response('regist.html',RST)


def logout(request):

    login_dic = request.session.get('IS_LOGIN',None)
    if login_dic:
        print login_dic
        username = login_dic['user']
        del request.session['IS_LOGIN']
        return redirect('/hostM/login/')
    return HttpResponse('no login')

@checklogin
def index(request):
    userdatas = models.AdminUser.objects.all()
    username = request.session['IS_LOGIN']['user']
    
    return render_to_response('index.html',{'userdatas':userdatas,'username':username})


##### 分页
def try_int(arg,default):
    try:
        result = int(arg)
    except Exception,e:
        result = default
    return result

@checklogin
def pages(request,cur_page):
    print request.COOKIES
    
    RST = {'datas':'','total':0,'username':'','htmls':''}
    
    user = request.session['IS_LOGIN']['user']
    RST['username'] = user
    
    datas = models.AdminUser.objects.all()
    ItemCount = datas.count()
    RST['total'] = ItemCount
    
    PerItems = try_int(request.COOKIES.get('page_num',3),3)
    CurPage = try_int(cur_page, 1)
    ItemSTR = (CurPage-1)*PerItems
    ItemEND = CurPage*PerItems
    RST['datas'] = datas[ItemSTR:ItemEND]
    
    PageTmp = divmod(ItemCount,PerItems)
    if PageTmp[1] != 0 :
        PageCount = PageTmp[0] + 1
    else:
        PageCount = PageTmp[0]
    
    PageHtmls = []
    FirstHtml = "<a href='/hostM/pages/%d'>首页</a>"%(1)
    PageHtmls.append(FirstHtml)
    
    if CurPage <= 1:
        PriHtml = "<a href='#'>上一页</a>"
    else:
        PriHtml = "<a href='/hostM/pages/%d'>上一页</a>"%(CurPage-1)
    PageHtmls.append(PriHtml)
    
    if PageCount < 12 :
        PageSTR = 1
        PageEND = PageCount
    else:
        if CurPage < 6:
            PageSTR = 0
            PageEND = 12
        else:
            if CurPage + 6 > PageCount:
                PageSTR = PageCount - 11
                PageEND = PageCount
            else:
                PageSTR = CurPage - 6
                PageEND = CurPage + 5

    for i in range(PageSTR,PageEND+1):
        if i == CurPage:
            html = "<a href='/hostM/pages/%d' class='selected'>%d</a>"%(i,i)
        else:
            html = "<a href='/hostM/pages/%d'>%d</a>"%(i,i)
        PageHtmls.append(html)
    
    if CurPage >= PageCount:
        NextHtml = "<a href='#'>下一页</a>"
    else:
        NextHtml = "<a href='/hostM/pages/%d'>下一页</a>"%(CurPage+1)
    PageHtmls.append(NextHtml)
    
    LastHtml = "<a href='/hostM/pages/%d'>尾页</a>"%(PageCount)
    PageHtmls.append(LastHtml)
    
    RST['htmls'] = mark_safe(''.join(PageHtmls))
    
    response = render_to_response('pages.html',RST)
    response.set_cookie('page_num',PerItems)
    return response