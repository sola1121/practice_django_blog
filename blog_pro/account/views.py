from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .form import LoginForm


# Create your views here.
def login_view(request):
    """自定义登录功能"""
    if request.method == "POST":
        login_form = LoginForm(request.POST)   # 直接使用Form接收POST中的字典数据
        if login_form.is_valid():   # 判断数据有效性
            cd = login_form.cleaned_data   # 获取有效数据
            user = authenticate(username=cd["username"], password=cd["password"])   # 鉴定是否存在User, 存在返回对象, 不存在返回None

            if user:
                login(request, user)   # 在request中留下一个用户id, 让通过验证的用户可以不用重复去验证, 利用session
                return HttpResponse("Welcome You, authenticated successfully.")
            else:
                return HttpResponse("Invalid login request.")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "self_account/account.html", {"form_obj": login_form})
