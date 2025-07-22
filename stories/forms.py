# stories/forms.py
from django import forms
from .models import Story
from django.utils import timezone
from django.core.exceptions import ValidationError

class StoryForm(forms.ModelForm):

    class Meta:
        model  = Story
        fields = ['media', 'caption']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user:
            now = timezone.now()
            if Story.objects.filter(user=self.user, expires_at__gt=now).exists():
                raise ValidationError("現在有効なストーリーがすでに存在します。削除されてから再度アップロードしてください。")
        return cleaned_data