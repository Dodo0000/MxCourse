# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/27'

from django.conf.urls import  url, include
from .views import UserInfoView



urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),

]