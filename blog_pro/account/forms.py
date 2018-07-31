from django import forms
from django.contrib.auth.models import User

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名:")
    password = forms.CharField(label="用户密码:", widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):                                       # 使用ModelForm, 将表单直接与model关联
    password = forms.CharField(label="用户密码:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码:", widget=forms.PasswordInput)

    class Meta:
        model = User                                                           # 本表单类所使用的数据模型, 及User数据表
        fields = ("username", "email")                                         # 选用的数据表字段, 也可用exclude列表说明
    
    def clean_password2(self):                                                 # 判断是否两次密码相等, 去人输入正误, 直接将方法写入表单
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Password don't match.")
        return cd["password2"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")
