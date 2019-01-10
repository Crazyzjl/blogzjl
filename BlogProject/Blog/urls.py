#__author:  Administrator
#date:   2018/12/31
from django.urls import path
from Blog import views
app_name = "Blog"

urlpatterns = [
    path(r"", views.index, name="index"),
    path(r"post/<int:pk>", views.detail, name="detail"),
]