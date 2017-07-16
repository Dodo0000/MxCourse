#/usr/bin/python
#coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/16'

from django.conf.urls import  url, include
from .views import OrgView, AddUserAskView


urlpatterns = [
    # 课程机构列表
    url(r'^list/$',OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask")
]
