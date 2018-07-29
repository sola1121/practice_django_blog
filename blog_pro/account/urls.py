from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views

from .form import LoginForm
from . import views

login_form = LoginForm()

urlpatterns = [
    # url(r"^login$", views.login_view, name="login"),

    url(r"^login$", auth_views.login, name="login"),   # 使用内置的登录功能, 其模板是在registration/login.html
    url(r"^self-login", auth_views.login, {"template_name": "self_account/account.html"}),   # 自定义template所在位置
]
