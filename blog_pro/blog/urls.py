from django.conf.urls import url
from blog.views import index_view, blog_content_view

urlpatterns = [
    url(r"/{0,1}$", index_view),
    url(r"/index/{0,1}$", index_view),

    url(r"/blog/(?P<blog_id>\d)$", blog_content_view),
]
