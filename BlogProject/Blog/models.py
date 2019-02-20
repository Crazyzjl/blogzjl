from django.db import models
import markdown
#strip_tags 去掉 HTML 文本的全部 HTML 标签
from django.utils.html import strip_tags
from django.contrib.auth.models import AbstractUser
from users.models import User

# from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    """文章数据库表"""

    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        #如果没有填写摘要
        if not self.excerpt:
            #实例化一个Markdown类， 用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #先将Markdown 文本渲染成 HTML 文本
            #strip_tags 去掉HTML 文本的全部HTML标签
            #从文本摘取前 54个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
    class Meta():
        ordering = ["-created_time"]
