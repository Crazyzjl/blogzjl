from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


#一定要在settings中设置自定义用户模型 AUTH_USER_MODEL = 'users.User'
#自定义User模型，继承AbstractUser获取他的全部属性，还可以拓展自己的属性
class User(AbstractUser):
    #记录用户的昵称，blank=True 可以让用户在注册时不用填写昵称
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_('email address'),
                              unique=True,
                              blank=True,
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                              }
                              )
    class Meta(AbstractUser.Meta):
        pass

#（不推荐）另一种拓展用户模型的模式，需要额外的夸表操作，这种方式比起直接继承 AbstractUser 效率更低一点
# class Profile(models.Model):
#     #这种模式有两张表：User模型表和Profile表
#     nickname = models.CharField(max_length=50, blank=True)
#     #关联django自带的User模型
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
