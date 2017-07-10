#/usr/bin/python
#coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/10'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)
    # 此处说明：在前端html中，表单的<input name="username">,<input name="password">
    # 其中,LoginFormz中的字段名字要与之对应