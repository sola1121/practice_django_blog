from django.contrib import admin

from .models import BlogArticle


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish", "author")
    search_fields = ("title",)


# Register your models here.
admin.site.register(BlogArticle, BlogArticleAdmin)

