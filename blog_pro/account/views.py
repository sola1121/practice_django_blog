from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import User, UserProfile, UserInfo
from .forms import LoginForm, RegistrationForm, UserForm, UserProfileForm, UserInfoForm


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
            # UserInfo.objects.create(user=new_user)
            return HttpResponse("regist successfully.")
        else:
            return HttpResponse("regist fialed.")
    if request.method == "GET":
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "self_account/register.html", {"form": user_form, "profile": userprofile_form})   # 用Get方式请求, 则将注册页面返回, 注意form的传递


@login_required(login_url="/account/login")   # 没有登录的用户会被转到该url
def myself(request):
# 查询出当前用户的相应信息
    user        = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.filter(user=user)
    userinfo    = UserInfo.objects.filter(user=user)

    return render(request, "self_account/myself.html", locals())


@login_required(login_url='/account/login/')
def myself_edit(request):
# 查询对应数据库中的相应数据
    user = User.objects.get(username=request.user.username) 
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
    # POST方法用于提交修改, 获取表单request.POST中的数据
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
        # 获取干净数据
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
        # 将新数据写入
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
        # 存入数据库
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')   
    else:
    # 实例化模型表单对象, 并给与对应的初值
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(
                initial={"birth":userprofile.birth, "phone":userprofile.phone}
            )
        userinfo_form = UserInfoForm(
                initial={"school":userinfo.school, "company":userinfo.company, 
                         "profession":userinfo.profession, "address":userinfo.address, 
                         "aboutme":userinfo.aboutme}
            )
        return render(request, "self_account/myself_edit.html", 
                     {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})


def my_image(request):
    """用户图片的处理视图"""
    if request.method == "POST":
        img = request.POST["img"]
        userinfo= UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, "self_account/imagecrop.html")
