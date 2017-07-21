# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/19'

from django.conf.urls import  url, include
from .views import CourseListView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list")

]