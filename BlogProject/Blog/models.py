from django.db import models
import markdown
#strip_tags 去掉 HTML 文本的全部 HTML 标签
from django.utils.html import strip_tags

# Create your models here.

#
# class Article(models.Model):
#     STATUS_CHOICES = (
#         ('d', 'Draft'),
#         ('p', 'Published')
#     )
#
#     title = models.CharField('标题', max_length=70)
#     body = models.TextField('正文')
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     last_modified_time = models.DateTimeField('修改时间', auto_now=True)
#     status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
#     abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
#                                 help_text='可选，如若为空将摘取正文的前54个字符')
#     views = models.PositiveIntegerField('浏览量', default=0)
#     likes = models.PositiveIntegerField('点赞数', default=0)
#     topped = models.BooleanField('置顶', default=False)
#
#     category = models.ForeignKey('Category', verbose_name='分类',
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#
#     def __str__(self):
#         return self.title
#     class Meta:
#         ordering = ['-last_modified_time']
#
# class Category(models.Model):
#     name = models.CharField('类名', max_length=20)
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     last_modified_time = models.DateTimeField('修改时间', auto_now=True)
#
#     def __str__(self):
#         return self.name
from django.contrib.auth.models import User
from django.urls import reverse
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
