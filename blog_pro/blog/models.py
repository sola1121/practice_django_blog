from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class BlogArticle(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, related_name="blog_posts")
    body = models.TextField(unique=True)
    publish = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-publish",)


