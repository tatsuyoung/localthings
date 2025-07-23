# stories/management/commands/delete_old_stories.py

from django.core.management.base import BaseCommand
from stories.models import Story
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

HOURS_TO_EXPIRE = settings.STORY_EXPIRE_HOURS # ストーリーの有効期限（時間）

class Command(BaseCommand):
    help = f"Delete stories older than {HOURS_TO_EXPIRE} hours"

    def handle(self, *args, **kwargs):
        cutoff     = timezone.now() - timedelta(hours=HOURS_TO_EXPIRE)
        deleted, _ = Story.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} old stories"))