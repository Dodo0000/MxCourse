# coding:utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email
# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # Q为or值，用户名=输入的用户名，或者邮箱等于输入的邮箱
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html", {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对明文密码进行加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,"register")
            return render(request,"login.html")
        else:
            return render(request,"register.html", {"register_form": register_form})




class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        # LoginForm()在传进来的时候有一个参数，这个参数为字典，request.POST就是一个字典
        # 所以此处一般传入request.POST内容
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 开始用类来写登入逻辑，LoginView类，所以这个user_login函数已丢弃
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg":"用户名或密码错误！"})
#     elif request.method == "GET":
#         return render(request,"login.html",{})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_sucess.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class RestView(View):
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不同"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email")
            return render(request, "password_reset.html",{"email": email, "modify_form": modify_form} )
