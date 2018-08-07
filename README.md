# 功能描述

1. 实现了从首页浏览所有已发博客的信息.
2. 实现了用户的登录注册功能.
3. 用户可以更改自己的密码.
4. 用户忘记密码可以通过其他注册信息重置密码.

# 知识点记录

## 静态文件的配置

在settings.py中做了如下修改

    STATIC_URL = '/static/'   # 指定url
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),   # 指定所在地址, 另外可以使用STATIC_ROOT
    ]

    # TEMPLATES 变量中
    ...
    'DIRS': [os.path.join(BASE_DIR, "templates")],   # 自定义模板位置
        'APP_DIRS': False,   # 关闭以默认方式查找模板
    ...

在需要使用的模板中{% load static %}载入静态文件, 模板中使用时直接使用{% static "静态文件路径" %}即可使用static中的文件

## 使用Django内置的登录

### django.contrib.auth.views中的login函数

    login(request, template_name='registration/login.html',
            redirect_field_name=REDIRECT_FIELD_NAME,
            authentication_form=AuthenticationForm,
            extra_context=None, redirect_authenticated_user=False)

其使用的表单为AuthenticateForm, 向指定的template_name中传递表单对象, 名为form.  
返回一个LoginView类对象, 用于显示一个login表单和处理相关事务.  
redirect_field_name是登录后重定向的位置, 可以在settings.py中添加LOGIN_REDIRECT_URL来指定位置.  
如果在模板中定义的action的位置, 那么跳转到其.

### django.contrib.auth.__init__中的login函数

    login(request, user, backend=None)

Persist a user id and a backend in the request. This way a user doesn't have to reauthenticate on every request. Note that data set during the anonymous session is retained when the user logs in.  
保留一个用户id和一个后端(session)在request中. 这样一个用户的每次request将不用重新鉴别. 注意在匿名session登录期间数据集任然保留.

### 使用authenticate方法验证用户

只限于用来验证User数据表中的相应用户字段, 有则返回相关对象, 无则返回None.

## 模板接收的参数

每次调用模板, 都会向模板发送一个request参数, 使用的render或其他方法传递.  
这个参数中记录了详尽的请求信息, 需要可以直接使用.
如, 使用django.contrib.auth.__init__中的login, 其就将验证后的用户直接放在了每次的request中.

## 使用内置的登出

### django.contib.auth.views.logout函数

    logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           extra_context=None)

默认使用的登出后重定向为registration/logged_out.html, 这是admin管理界面的, 当然, login那个模板也是用的admin的.  
如同django.contrib.auth.views.login一样, logout也可以在参数中更改其重定向的模板.
返回的是一个LogoutView对象.

### django.contrib.auth.__init__中的logout函数

    logout(request)

Remove the authenticated user's ID from the request and flush their session data.  
从request中移除已经验证的用户id,并刷新他们的session数据.

## 注册使用ModelForm类

注册针对用户可能有多种要求, 所以django中没有内置的注册方法.  
这是一个可以直接和数据表关联的表单对象, 通过在Meta类中的model参数中设置关联的数据库对象, 在fields中设置使用的数据表字段.

### 拓展django.contrib.auth.models.User内置数据库表

    添加一个一对一的OneToOneField外键表, 关联后就可以, 新增一些字段.

## 修改密码

django有内置的修改密码相关的方法, 可以拿来直接用.  
在django.contrib.auth.views中, 有password_change, password_change_done两个与密码修改相关的函数.

    password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None)

可见password_change使用的模板是registration/password_change_form.html, 使用的ModelForm表单设计PassWordChangeForm
其向模板中传入`context={'form': form, 'title': _('Password change')}`  

    password_change_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None)

password_change_done是当更改完成后系统应该调用的方法, 主要用于提示用户.  
在extra_context中可以添加额外的内容到context中.

**注意**: post_change_redirect, 这是重定向到password_change_done的配置参数, 使用了django.urls.base中的reverse相关方法
reverse方法用于将给定的 _namespace: name_ 形式的字符串转换为url地址, 如果配置未成功, 会造成如下错误

    Reverse for 'password_change_done' not found.

## 重置密码, 用于用户忘记密码的时候

在django.contrib.auth.views中提供了一个密码重置的解决方案, 使用password_reset的一系列函数, 通过邮件来重置密码.
>向用户发送邮件 -> 显示发送是否成功      -> 使用邮箱中的url重置密码 -> 如果成功,显示成功信息  
>password_reset-> password_reset_done -> password_reset_confirm-> password_reset_complete  
发送邮件: password_reset_form.html,  
邮件内容: password_reset_email.html,  
邮件发送成功: password_reset_done.html,  
密码被确认: password_reset_confirm.html,  
密码重置完成: password_reset_complete.html.

    password_reset(request,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None)

template_name是发送邮件的表单模板, 使用password_reset_form.html模板.  
email_template_name发送给用户的邮件内容所在模板. 一般其中有一条向password_reset_confirm模板请求的连接. 这是邮件内容的模板.password_reset_email.html  
向模板中传递`context = {'form': form, 'title': _('Password reset')`, form是在django.contrib.auth.form中的 PasswordResetForm(forms.Form)对象, 只有一个forms.EmailField字段  
subject_template_name描述路径的文件中的内容将是所发邮件的主题.
post_reset_redirect指明跳转目标.

    password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        extra_context=None)

template_name是完成发送使用的模板, 为password_reset_done.html

    password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None)

uidb64是散列的用户id
token是在连接中由password_reset中的token_generator=default_token_generator, 来自

    django.contrib.auth.tokens.PasswordResetTokenGenerator(object)
        """
        Strategy object used to generate and check tokens for the password
        reset mechanism.
        """

    password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None)

完成后请求password_reset_complete.html

**注意:**邮箱只能是在auth_user中有的邮箱地址, django会在发送时检验是否存在该邮箱.

### 重置密码的url配置

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

### 配置邮箱

在settings.py中

    # 配置邮箱
    # qq IMAP/SMTP 配置
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.qq.com'
    EMAIL_PORT = 25                          # 或者 465/587是设置了 SSL 加密方式
    # 发送邮件的邮箱
    EMAIL_HOST_USER = "3342076252@qq.com"
    # 在邮箱中设置的客户端授权密码
    EMAIL_HOST_PASSWORD = "IMAP授权码"        # 如果重新设置了新的授权码,直接使用最新的授权码即可
    EMAIL_USE_TLS = True                      # 这里必须是 True，否则发送不成功
    # 收件人看到的发件人, 必须是一直且有效的
    EMAIL_FROM = 'Tencent<3342076252@qq.com>'

### 使用第三方库重置密码

sudo pip install django-password-reset  
在settings.py的应用(INSTALLED_APP)中添加"password_reset", 即添加应用, 在根中的urlpatterns中添加地址  
第三方的应用依然遵循django的开发方式, 就是view, form, urls, templates 的集合, 以下是其urls  

    urlpatterns = [
        url(r'^recover/(?P<signature>.+)/$', views.recover_done, name='password_reset_sent'),
        url(r'^recover/$', views.recover, name='password_reset_recover'),
        url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
        url(r'^reset/(?P<token>[\w:-]+)/$', views.reset, name='password_reset_reset'),
    ]

## 个人信息展示

    def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
        """
        Decorator for views that checks that the user is logged in, redirecting
        to the log-in page if necessary.
        """
        # 用于在view中检查用户是否登录的装饰器, 在需要时可以指定重定向到log-in页面.

## 编辑个人信息

使用forms.ModelForm表单类, 直接与models相对接. 涉及到 urls, forms, views, templates之间的配置.  
    