# stories/views.py
import os
import uuid
from .utils import trim_video, compress_video
from django.core.files import File
from .models import Story, StoryRead
from .forms import StoryForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from functools import wraps

HOURS_TO_EXPIRE    = settings.STORY_EXPIRE_HOURS # ストーリーの有効期限（時間）
MAX_VIDEO_DURATION = settings.MAX_VIDEO_DURATION  # 最大動画長さ（秒）
User               = get_user_model()

@login_required
def story_create(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            media_file = request.FILES.get("media")
            caption    = form.cleaned_data.get("caption", "")

            if media_file:
                temp_input_path      = f"/tmp/{uuid.uuid4()}_{media_file.name}"
                temp_trimmed_path    = f"/tmp/trimmed_{uuid.uuid4()}.mp4"
                temp_compressed_path = f"/tmp/compressed_{uuid.uuid4()}.mp4"

                # 一時保存
                with open(temp_input_path, "wb") as f:
                    for chunk in media_file.chunks():
                        f.write(chunk)

                # ✅ トリミング
                success_trim = trim_video(temp_input_path, temp_trimmed_path, max_duration=MAX_VIDEO_DURATION)

                if success_trim:
                    # ✅ 圧縮
                    success_compress = compress_video(temp_trimmed_path, temp_compressed_path)

                    if success_compress:
                        with open(temp_compressed_path, "rb") as f:
                            django_file = File(f)
                            story = Story(
                                user=request.user,
                                media=django_file,
                                caption=caption,
                                expires_at=timezone.now() + timedelta(hours=HOURS_TO_EXPIRE),
                            )
                            story.save()

                # 一時ファイル削除
                for path in [temp_input_path, temp_trimmed_path, temp_compressed_path]:
                    if os.path.exists(path):
                        os.remove(path)

            return redirect("articles:list")
        else:
            # フォームが無効な場合（有効なストーリーが存在など）
            for error in form.non_field_errors():
                messages.error(request, error)  # エラーメッセージを表示
            return redirect("articles:list")  # リダイレクト
    else:
        # GETリクエストはリダイレクト
        return redirect("articles:list")


# Delete
@require_POST
@login_required
def story_delete_ajax(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.user != story.user:
        return JsonResponse({"success": False, "message": "このストーリーは削除できません。"}, status=403)

    story.delete()
    return JsonResponse({"success": True, "message": "ストーリーを削除しました。"})

# 特定ユーザーの有効な（期限切れでない）ストーリー一覧を取得して表示
@login_required
def story_view(request, user_id):
    stories = Story.objects.filter(user_id=user_id, 
    expires_at__gt=timezone.now()
    ).order_by('created_at')
    return render(request, 'stories/story_view.html', {'stories': stories})



# Ajaxなどから呼び出して、「ユーザーがこのストーリーを見た」というログ（ManyToMany的な）を記録
@login_required
def mark_story_read(request, story_id):
    if request.method == "GET":
        try:
            story = Story.objects.get(id=story_id)
            StoryRead.objects.get_or_create(user=request.user, story=story)
            return JsonResponse({"status": "ok"})
        except Story.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Story not found"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)

