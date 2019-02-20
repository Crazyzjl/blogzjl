#!/usr/bin/python3
# coding    : utf-8
# @Time     : 2019/2/1 15:05
# @FileName : urls.py
# @Software : PyCharm

from django.contrib import admin
from django.urls import path
from users import views


app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
]
