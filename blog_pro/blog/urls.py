from django.conf.urls import url
from .views import index_view

urlpatterns = [
    url(r"/{0,1}$", index_view),
    url(r"index/{0,1}$", index_view),
]
