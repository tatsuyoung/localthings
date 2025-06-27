from django import forms
from . import models
from .models import ArticleImage

class CreateArticle(forms.ModelForm):
    class Meta:
        model   = models.Article
        exclude = ['title', 'date', 'author']  # ← fieldsの代わりに exclude
        widgets = {
            "slug"    : forms.HiddenInput(), 
            "body"    : forms.Textarea(attrs={"class": "edit-article-body-textarea"}),
            "category": forms.Select(attrs={"class": "edit-article-category-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'No Category'


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model  = ArticleImage
        fields = ['image']


class CommentForm(forms.ModelForm):
    class Meta:
        model   = models.Comment
        fields  = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': 'Write your comment here'}),
        }