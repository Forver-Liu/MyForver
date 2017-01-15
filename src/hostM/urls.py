"""work1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views_clc,views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'plug/(?P<a>\d+)/(?P<b>\d+)/',views_clc.plug1),
    url(r'plug/$',views_clc.plug2),
    
    url(r'adduser/$',views.adduser),
    url(r'addusertype/$',views.addUserType),
    
    url(r'login/$',views.login),
    url(r'regist/$',views.regist),
    url(r'index/$',views.index),
    url(r'logout/$',views.logout),
    
    url(r'pages/(\d*)',views.pages),
]
