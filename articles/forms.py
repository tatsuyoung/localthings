from django import forms
from . import models
from .models import Category


class CreateArticle(forms.ModelForm):

    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumb', 'category', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'No Category'


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': 'Write your comment here'}),
        }