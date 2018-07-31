from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegistrationForm, UserProfileForm


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


def register_view(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)                    # 调用ModelForm对象的save方法, 将直接把内容提交至数据库, 这里设置为False
            new_user.set_password(user_form.cleaned_data["password"])  # 设置了对象密码(未检验的)
            new_user.save()                                            # 在次保存, 这下将数据保存至数据库了.
            return HttpResponse("regist successfully.")
        else:
            return HttpResponse("regist fialed.")
    if request.method == "GET":
        user_form = RegistrationForm()
        return render(request, "self_account/register.html", {"form": user_form})   # 用Get方式请求, 则将注册页面返回, 注意form的传递


def register_view2(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid():
            print("所获得的有效数据", user_form.cleaned_data, userprofile_form.cleaned_data)
        # 对User填入数据
            new_user = user_form.save(commit=False)                    
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
        # 对userprofile填入数据
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse("regist successfully.")
        else:
            return HttpResponse("regist fialed.")
    if request.method == "GET":
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "self_account/register.html", {"form": user_form, "profile": userprofile_form})   # 用Get方式请求, 则将注册页面返回, 注意form的传递
