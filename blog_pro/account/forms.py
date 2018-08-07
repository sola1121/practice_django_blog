from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, UserInfo

class LoginForm(forms.Form):
    """登录用的表单"""
    username = forms.CharField(label="用户名:")
    password = forms.CharField(label="用户密码:", widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):                                       # 使用ModelForm, 将表单直接与model关联
    """用户更改密码的表单"""
    password = forms.CharField(label="用户密码:", widget=forms.PasswordInput)   # 新增的表单列 
    password2 = forms.CharField(label="确认密码:", widget=forms.PasswordInput)  # 新增的表单列

    class Meta:
        model = User                                                           # 本表单类所使用的数据模型, 及User数据表
        fields = ("username", "email")                                         # 选用的数据表字段, 也可用exclude列表说明
    
    def clean_password2(self):                                                 # 判断是否两次密码相等, 去人输入正误, 直接将方法写入表单
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Password don't match.")
        return cd["password2"]


class UserProfileForm(forms.ModelForm):
    """UserProfile对应的表单"""
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    """UserInfo对应的表单"""
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")
    
    def get(self, a):
        return "我看看这个get是在哪调用的.%s" %a


class UserForm(forms.ModelForm):
    """User主表对应的表单类"""
    class Meta:
        model = User
        fields = ("email",)

