#!/usr/bin/python3
# coding    : utf-8
# @Time     : 2019/2/1 14:10
# @FileName : forms.py
# @Software : PyCharm

#需要修改 Meta 中的model ，默认关联django中的User模型
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        #修改默认model
        model = User
        #显示用于注册的表单，password在父类中实现了，还需要用户提供"username", "email"
        fields = ("username", "email")