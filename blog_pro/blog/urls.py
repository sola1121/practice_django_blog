from django.conf.urls import url
from blog.views import index_view, blog_content_view

urlpatterns = [
    url(r"^$", index_view),
    url(r"^index$", index_view),

    url(r"^blog/(?P<blog_id>\d)$", blog_content_view),
]
