# coding:utf-8

__Author__ = 'eyu Fanne'
__Date__ = '2017/7/27'

from django.conf.urls import  url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEamilCodeView, UpdateEmailView



urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEamilCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

]