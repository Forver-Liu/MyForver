#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response
from django.http import HttpResponse

# Create your views here.

def plug1(request,a,b):
    print request
    c = int(a) + int(b)
    print c
    return HttpResponse(str(c))

def plug2(request):
    print request
    A = request.GET['a']
    B = request.GET['b']
    C = int(A) + int(B)
    print C
    return HttpResponse(str(C))