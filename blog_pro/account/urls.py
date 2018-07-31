from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from . import views

login_form = LoginForm()

app_name = "account"

urlpatterns = [
    # login相关
    url(r"^login$", views.login_view, name="login"),
    url(r"^dj-login1$", auth_views.login, name="dj-login1"),   # 使用内置的登录功能, 其模板是在registration/login.html
    url(r"^dj-login2$", auth_views.login, {"template_name": "self_account/account.html"}, name="dj-login2"),   # 自定义template所在位置

    # logout相关
    url(r"^dj-logout$", auth_views.logout, {"template_name": "self_account/logout.html"}, name="dj-logout"),   # 自定义template所在位置

    # register相关
    url(r"^register", views.register_view2, name="register"),

    # 修改密码 TODO: 未完成
    url(r"^change-pass", auth_views.password_change, {"template_name": "registration/password_change_form.html"}),
]
