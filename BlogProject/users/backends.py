#!/usr/bin/python3
# coding    : utf-8
# @Time     : 2019/2/1 17:22
# @FileName : backends.py
# @Software : PyCharm

from .models import User

#自定义email登录验证，需要在settings设置
class EmailBackend(object):
    def authenticate(self, request, **credentials):
        #要注意登录表单中用户输入的用户名或者邮箱的field名均为username
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        """
        该方法是必须的
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None