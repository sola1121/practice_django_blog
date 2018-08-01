# 功能描述

1. 实现了从首页浏览所有已发博客的信息.
2. 实现了用户的登录注册功能.
3. 用户可以更改自己的密码.
4. 用户忘记密码可以通过其他注册练习信息重置密码.

# 知识点记录

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

    def password_change_done(request,
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

template_name是发送邮件的表单模板.

    password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        extra_context=None)

    password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None)
    
    password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None)