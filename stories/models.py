# models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

HOURS_TO_EXPIRE = settings.STORY_EXPIRE_HOURS # ストーリーの有効期限（時間）

User = get_user_model()

def story_video_upload_path(instance, filename):
    return f'stories/{instance.user.id}/{filename}'


class Story(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    media      = models.FileField(upload_to=story_video_upload_path)
    caption    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=HOURS_TO_EXPIRE)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.user.username}'s Story ({self.created_at})"

class StoryRead(models.Model):
    story   = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='reads')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_reads')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')  # 同じユーザーが同じ Story を何回読んでも1件だけ