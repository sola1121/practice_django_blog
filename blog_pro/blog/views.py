import os

from django.shortcuts import render

from .models import BlogArticle

# Create your views here.
def index_view(request):
    blogs = BlogArticle.objects.all()
    return render(request, os.path.dirname(__file__) + "/index.html", {"blogs": blogs})