#!/usr/bin/python3
# coding    : utf-8
# @Time     : 2019/1/18 17:43
# @FileName : feeds.py
# @Software : PyCharm

from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    #显示在聚合阅读器上的标题
    title = "一点点"
    #通过聚合阅读器跳转到网站的地址
    link = "/"
    #显示在聚合阅读器上的描述信息
    description = "记录你生活的每一点点"

    #需要显示的内容条目
    def items(self):
        return Post.objects.all()

    #聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    #聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body
