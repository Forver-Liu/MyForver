#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.core import serializers

import models
import time
import json
from datetime import date, datetime
from process1.models import News
# Create your views here.

def adddatas(request):
    UserTypeObj = models.UserType.objects
    UserTypeObj.create(display='admin')
    UserTypeObj.create(display='reader')
    #UserTypeObj.save()
    print "UserTypeObj"
    time.sleep(1)
    
    UserObj = models.Admin.objects
    UserObj.create(username="admin",password="admin",email="",user_type=UserTypeObj.filter(id=1))
    UserObj.create(username="reader",password="reader",email="",user_type=UserTypeObj.filter(id=2))
    print "UserObj"
    time.sleep(1)
    
    ChatObj = models.Chat.objects
    ChatObj.create(content='hello',user=UserTypeObj.filter(id=1))
    ChatObj.create(content='hell2',user=UserTypeObj.filter(id=2))
    print "ChatObj"
    time.sleep(1)
    
    NewsTypeObj = models.NewsType.objects
    NewsTypeObj.create(display='IT')
    NewsTypeObj.create(display='cars')
    NewsTypeObj.create(display='left')
    print "NewsTypeObj"
    time.sleep(1)
    
    NewsObj = models.News.objects
    NewsObj.create(title='title1',summary='title1 summary',url="http://www.baidu.com",news_type=NewsTypeObj.filter(id=1),user=UserTypeObj.filter(id=1))
    NewsObj.create(title='title2',summary='title2 summary  yunyun',url="http://www.baidu.com",news_type=NewsTypeObj.filter(id=2),user=UserTypeObj.filter(id=2))
    print "NewsObj"
    time.sleep(1)
    
    ReplyObj = models.Reply.objects
    ReplyObj.create(content='title1 reply1',user=UserTypeObj.filter(id=2),news=NewsObj.filter(id=1))
    ReplyObj.create(content='title1 reply2',user=UserTypeObj.filter(id=1),news=NewsObj.filter(id=1))
    print "ReplyObj"
    time.sleep(1)
    
    return HttpResponse("add datas successful")

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



def index(request):
    RST = {'stat':0,'data':''}
    
    NewsObj = models.News.objects
    AllNews = NewsObj.all()
    
    RST['data']=AllNews
    return render_to_response("index.html",RST)

def addfavor(request):
    RST = {'stat':0,'data':'','message':''}
    
    try:
        nid = request.POST.get('nid',0)
        print nid
        NewsObj = models.News.objects.get(id=nid)
        tmp = NewsObj.favor_count + 1
        NewsObj.favor_count = tmp
        NewsObj.save()
        
        RST['stat'] = 0
        RST['data'] = tmp
        RST['message'] = "ok"
    except Exception,e:
        print e.message
        RST['stat'] = 1
        RST['data'] = None
        RST['message'] = e.message
        
    return HttpResponse(json.dumps(RST))

def getreply(request):
    RST = {'stat':0,'data':'','message':''}
    
    if request.method == "POST":
        try:
            id = request.POST.get('nid')
            print id
            replysObj = models.Reply.objects.filter(news__id=id).values('id','content','create_date','user__username')[0]
            print type(replysObj)
            #reply_list = serializers.serialize("json", replysObj)
            reply_list = json.dumps(replysObj,cls=MyEncoder)
            print reply_list
            RST['data'] = reply_list
            RST['stat'] = 0 
        except Exception,e:
            RST['stat'] = 1
            print "get replays failed"
            RST['message'] = e.message
        finally:
            result = json.dumps(RST)
            print result
            return HttpResponse(json.dumps(RST))
    else:
        RST['stat'] = 1
        RST['message'] = "request must post"
        return HttpResponse(json.dumps(RST))
    
def submitreply(request):
    RST = {'stat':0,'data':'','reply_count':'','message':''}
    
    NewID = request.POST.get('nid')
    content =  request.POST.get('data')
    RST['data'] = content
    try:
        uid = request.session['login_user']['uid']
    except Exception,e:
        RST['stat'] = 1
        RST['message'] = "not login"
        return HttpResponse(json.dumps(RST))
        
    ReplyObj = models.Reply.objects
    ReplyObj.create(content=content,
                    user=models.Admin.objects.get(id=uid),
                    news=models.News.objects.get(id=NewID)
                    )
    NewsObj = models.News.objects
    tmp = NewsObj.get(id=NewID).id + 1
    NewsObj.get(id=NewID).id = tmp
#    NewsObj.save()
    RST['reply_count'] = tmp
    
    return HttpResponse(json.dumps(RST))
     
        
def login(request):
    if request.method == "POST":
        user = request.POST.get('username')
        passwd = request.POST.get('password')
        
        AdminObj = models.Admin.objects
        try:
            cur_user = AdminObj.get(username=user,password=passwd)
        except Exception,e:
            cur_user = None
        if cur_user:
            print "loginedd"
            uid = cur_user.id
            request.session['login_user'] = {'uid':uid}
            return redirect('/process1/index/')
        else:
            return render_to_response('login.html')
    else:
         return render_to_response('login.html')   
     
def chat(request):
    
    return render_to_response('chat.html')

def subchat(request):
    RST = {'stat':0,'data':'','message':''}
    
    if request.method == "POST":
        content = request.POST.get('data')
        uid = request.session['login_user']['uid']
    
        chatObj = models.Chat.objects
        adminObj = models.Admin.objects
        try:
            userObj = adminObj.get(id=uid)
            print userObj.username
            contentObj = chatObj.create(contents=content,user=userObj)
            print contentObj
            time = contentObj.create_date

            RST['data'] = {
                           'id':contentObj['id'],
                           'username':userObj.username,
                          # 'content':contentObj.content,
                           'create_date':time,
                           }
            print RST['data']
        except Exception,e:
            RST['stat'] = 1
            RST['message'] = e.message
        finally:
            return HttpResponse(json.dumps(RST,cls=MyEncoder))
    else:
        return render_to_response('login.html')
    
def getchats(request):
    RST = {'stat':0,'data':'','message':''}
    
    if request.method == "GET":
        chatsObj = models.Chat.objects.all().order_by('-id').values('id','content','user__username','create_date')[0:10]
        print type(chatsObj)
        
        chats_list =  list(chatsObj)
        print "List:%s"%chats_list
        RST['data'] = chats_list
        
        RST['last_id'] = chatsObj[0]['id']
        print RST['last_id']
        print RST['data']
        return HttpResponse(json.dumps(RST,cls=MyEncoder))

    else:
        RST['stat'] = 1
        RST['message'] = "need post request"
        return HttpResponse(json.dumps(RST))
    
def getchats2(request):
    RST = {'stat':0,'data':'','message':''}
    
    lastID = request.GET.get('lastid')
    chatsObj = models.Chat.objects.filter(id__gt=lastID).values('id','content','user__username','create_date')
    chats_list =  list(chatsObj)
    
    RST['data'] = chats_list
    return HttpResponse(json.dumps(RST,cls=MyEncoder))