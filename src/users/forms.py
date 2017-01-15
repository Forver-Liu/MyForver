#!/usr/bin/env python
#coding:utf-8

from django import forms
from .models import admins


class loginF(forms.Form):
    username = forms.CharField(max_length=150,error_messages={'required':u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(),error_messages={'required':u'密码不能为空'})
    
    def clean_username(self):
        data = self.cleaned_data['username']
        is_exit = admins.objects.filter(username=data).exists()
            
        if not is_exit:
            raise forms.ValidationError(u'用户名不存在')
        return data

class registF(forms.Form):
    username = forms.CharField(label="用户名",max_length=100,required=True,error_messages={'required':u'用户名不能为空'})
    password = forms.CharField(label="密     码",widget=forms.PasswordInput(),required=True,error_messages={'required':u'密码不能为空'})
    email = forms.EmailField(label="邮箱",required=True,error_messages={'required':u'邮箱不鞥为空','invalid':u'内容无效，邮箱格式错误'})
    phone = forms.IntegerField(label='联系电话',required=True,error_messages={'required':u'联系电话不鞥为空'})
    infos = forms.CharField(label='备注',max_length=500,required=None)
    #usertype = forms.ChoiceField(label='用户类型',required=True,choices=(('leve1','admin'),('leve2','superadmin')))
    

    
class regist(forms.ModelForm):
    class Meta:
        model = admins
        #fields = '__all__'
        fields = ('username','password','email','phonenum','userinfos','usertype')