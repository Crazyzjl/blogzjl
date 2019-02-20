#__author:  Administrator
#date:   2018/12/31
from django.urls import path, include
from Blog import views
app_name = "Blog"

urlpatterns = [
    path(r"", views.IndexView.as_view(), name="index"),
    path(r"post/<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path(r"category/<int:pk>/", views.CategoryView.as_view(), name="category"),
    path(r"tag/<int:pk>/", views.TagView.as_view(), name="tag"),
    path(r"archives/<int:year>/<int:month>/", views.ArchivesView.as_view(), name="archives"),
    # path(r"search/", views.search, name="search"),
]
