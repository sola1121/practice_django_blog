from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .form import LoginForm


# Create your views here.
def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)   # 直接使用Form接收POST中的字典数据
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd["the_name"], password=cd["the_pass"])   # 鉴定是否存在User

            if user:
                login(request, user)
                return HttpResponse("Welcome You, authenticated successfully.")
            else:
                return HttpResponse("Invalid login request.")

    if request.method == "GET":
        login_form = LoginForm()
        
        return render(request, "self_account/account.html", {"form_obj": login_form})
