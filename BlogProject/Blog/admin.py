from django.contrib import admin
from .models import Post, Category, Tag, VisitNumber, DayNumber, UserIp
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

class UserIpAdmin(admin.ModelAdmin):
    list_display = ['ip_addr', 'ip', 'end_point', 'count']

class DayNumberAdmin(admin.ModelAdmin):
    list_display = ['day', 'count']

class VisitNumberAdmin(admin.ModelAdmin):
    list_display = ['count']

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(VisitNumber, VisitNumberAdmin)
admin.site.register(DayNumber, DayNumberAdmin)
admin.site.register(UserIp, UserIpAdmin)
