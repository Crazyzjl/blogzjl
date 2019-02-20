#__author:  Administrator
#date:   2019/1/6

from django import forms
from .models import Comment
from django.forms import formset_factory

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

CommentFormSet = formset_factory(CommentForm, max_num=1)