#__author:  Administrator
#date:   2019/1/6
from django.urls import path
from . import views
app_name = 'comments'

urlpatterns = [
    path(r'post/<int:pk>/', views.post_comment, name='post_comment'),

]