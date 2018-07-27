from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BlogArticle

# Create your views here.
def index_view(request):
    blogs = BlogArticle.objects.all()
    return render(request, "index.html", {"blogs": blogs})


def blog_content_view(request, blog_id):
    blog = get_object_or_404(BlogArticle, id=blog_id)
    return render(request, "blog.html", {"blog_title": blog.title, "blog_content": blog.body})
