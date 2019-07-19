from django import forms
from. import models


class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumb', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']