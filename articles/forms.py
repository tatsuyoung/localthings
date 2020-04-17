from django import forms
from . import models
from .models import Category


class CreateArticle(forms.ModelForm):

    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumb', 'category', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': 'Write your comment here'}),
        }