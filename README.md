# 功能描述

1. 实现了从首页浏览所有已发博客的信息.
2. 实现了用户的登录注册功能.

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

## 模板接收的参数

每次调用模板, 都会向模板发送一个request参数, 使用的render或其他方法传递.  
这个参数中记录了详尽的请求信息, 需要可以直接使用.
如, 使用django.contrib.auth.__init__中的login, 其就将验证后的用户直接放在了每次的request中.