#__author:  Administrator
#date:   2019/1/4

from ..models import Post, Category, Tag, VisitNumber, DayNumber, UserIp
from django.db.models.aggregates import Count
from Blog import models
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    '''
    获取最近的文章
    :param num: 默认最近5个
    :return: 最近的num篇文章
    '''
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    '''
    按月份归档
    :return: dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）
    的创建时间，且是 Python 的 date 对象，精确到月份，降序排列
    '''
    return Post.objects.dates("created_time", "month", order='DESC')

@register.simple_tag
def get_categories():
    '''
    分类标签
    '''
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    """标签云"""

    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_model(model_class):
    cls = getattr(models,model_class,"")
    print("model_class", model_class)
    counts = 0
    if cls:
        instance = cls.objects.order_by("-id")
        counts = instance[0].count + 1
        # print("count----",counts)
    return counts
