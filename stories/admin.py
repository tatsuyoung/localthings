# stories/admin.py
from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_expired']