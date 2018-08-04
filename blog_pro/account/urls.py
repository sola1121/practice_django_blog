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
    url(r"^register$", views.register_view2, name="register"),

    # 修改密码
    # 这里如果指定的话, 会使用默认的template_name, 为registration/password_change_...
    url(r"^change-pass$", auth_views.password_change, 
                        {"template_name": "self_account/password_change_form.html",
                         "post_change_redirect": "/account/change-pass-done"},   # 这是url, 解决 Reverse for 'password_change_done' not found
                        name="change_pass"),
    url(r"^change-pass-done$", auth_views.password_change_done, 
                            {"template_name": "self_account/password_change_done.html"}, 
                            name="change_pass_done"),

    # 密码重置相关, 4个方法 , 5个模板
    url(r"^password-reset$", auth_views.password_reset, 
                             {"template_name": "self_account/password_reset_form.html",           # 设置重设表单模板
                              "email_template_name": "self_account/password_reset_email.html",    # 设置email内容模板
                              "subject_template_name": "self_account/password_reset_subject.txt", # 该文件中的内容就是邮件发送的主题
                              "post_reset_redirect": "/account/password-reset-done"               # 这是url, 成功时重定向到下一个地址
                             },
                             name="password_reset"),
    url(r"^password-reset-done$", auth_views.password_reset_done,
                                 {"template_name":"self_account/password_reset_done.html"},   # 设置完成邮件发送时的重定向到的模板
                                 name="password_reset_done"),
    url(r"^password-reset-comfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$", auth_views.password_reset_confirm,
                                                                           {"template_name": "self_account/password_reset_confirm",     # 设置确认邮件模板
                                                                            "post_reset_redirect": "/account/password-reset-complete"}, # 这是url, 成功后重定向地址
                                                                            name="password_reset_confirm"),
    url(r"^password-reset-complete$", auth_views.password_reset_complete, 
                                      {"template_name": "self_account/password_reset_complete"},   # 设置完成重置密码后使用模板
                                      name="password_reset_complete"),
    
    # 用户信息相关
    url(r"my-information", views.myself, name="my_information"),
]
