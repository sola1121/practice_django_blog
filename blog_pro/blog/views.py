from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import BlogArticle

# Create your views here.
def index_view(request):
    blogs = BlogArticle.objects.all()
    return render(request, "index.html", {"blogs": blogs})


def blog_content_view(request):
    if request.method == "GET":
        blog_id = request.GET.get("log_id", None)
    if not blog_id:
        return
    blog = get_object_or_404(BlogArticle.objects.filter(id=blog_id))
    return render(request, "index.html", {"blog_content": blog.body})
    # return HttpResponse(blog.body)
