from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from notifications.signals import notify

import os
import pillow_heif
pillow_heif.register_heif_opener()

from PIL import Image, ImageOps, ExifTags
from io import BytesIO

import logging
logger = logging.getLogger(__name__)

from django.urls import reverse
          
 
class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
            notify.send(
                user,
                recipient=profile_.user,
                verb='さんが、あなたをフォローしました。',
                action_object=profile_,
                data={'url': reverse('accounts:profile_detail', kwargs={'username': user.username})}
            )
        return profile_, is_following


class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pics',
                              help_text='著作権を確認してください。')
    bg        = models.ImageField(upload_to='user_background', blank=True, null=True, help_text='著作権を確認してください。')
    bio       = models.TextField(max_length=160, blank=True, null=True)
    website   = models.URLField(max_length=250,  blank=True, null=True)
    # フォロワー = このユーザーをフォローしているUser
    followers = models.ManyToManyField(User, related_name='following_users', blank=True)
    objects   = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile'

    # saveメソッドをオーバーライドして画像処理を追加
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if not self.id:
            self.set_image()
        else:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image:
                self.set_image()
        if not self.id:
            self.set_bg()
        else:
            this = Profile.objects.get(id=self.id)
            if this.bg != self.bg:
                self.set_bg()
        return super().save(*args, **kwargs)


    def set_image(self):
        try:
            if not self.image or self.image.name == 'default.png':
                return

            self.image.seek(0)
            pil_image = Image.open(BytesIO(self.image.read()))

            # EXIFのOrientation取得と回転補正（JPEGのみ）
            if hasattr(pil_image, "_getexif"):
                exif = pil_image._getexif()
                if exif:
                    exif = dict(exif.items())
                    orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None)
                    orientation = exif.get(orientation_key)
                    if orientation == 3:
                        pil_image = pil_image.rotate(180, expand=True)
                    elif orientation == 6:
                        pil_image = pil_image.rotate(270, expand=True)
                    elif orientation == 8:
                        pil_image = pil_image.rotate(90, expand=True)

            # 📐 アスペクト比を維持しつつ 192x192 正方形にトリミング & リサイズ
            target_size = (192, 192)
            pil_image = ImageOps.fit(pil_image, target_size, Image.Resampling.LANCZOS)

            # 💾 JPEG形式で保存
            output = BytesIO()
            pil_image.save(output, format="JPEG", quality=70, optimize=True)
            output.seek(0)

            # 🔤 拡張子を .jpg にして再保存
            base = os.path.splitext(self.image.name)[0]
            filename = base + ".jpg"
            self.image.delete(save=False)
            self.image.save(filename, File(output), save=False)

        except Exception as e:
            logger.error(f"set_image error: {e}")


    def set_bg(self):
        try:
            if not self.bg:
                return
            self.bg.seek(0)
            pil_image = Image.open(BytesIO(self.bg.read()))

            # EXIFのOrientation取得（JPEGのみ）
            exif = None
            if hasattr(pil_image, "_getexif"):
                exif = pil_image._getexif()
                if exif is not None:
                    exif = dict(exif.items())
                    orientation = None
                    for key, value in ExifTags.TAGS.items():
                        if value == 'Orientation':
                            orientation = key
                            break
                    # 回転
                    if orientation in exif:
                        if exif[orientation] == 3:
                            pil_image = pil_image.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            pil_image = pil_image.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            pil_image = pil_image.rotate(90, expand=True)

            # アスペクト比によるリサイズ処理
            original_width, original_height = pil_image.size
            aspect_ratio = original_width / original_height

            # 推奨サイズ（例：Feed用）に合わせる
            if aspect_ratio > 1.91:
                target_size = (1080, int(1080 / 1.91))  # 横長
            elif aspect_ratio < 0.8:
                target_size = (1080, 1350)              # 縦長
            else:
                target_size = (1080, 1080)              # 正方形

            pil_image = ImageOps.fit(pil_image, target_size, Image.Resampling.LANCZOS)

            # 最終保存処理
            output = BytesIO()
            pil_image.save(output, format="JPEG", quality=70, optimize=True)
            output.seek(0)

            # ファイル名を明示的にjpgに
            base = os.path.splitext(self.bg.name)[0]
            filename = base + ".jpg"
            self.bg.delete(save=False)  # 古いファイルを削除
            self.bg.save(filename, File(output), save=False)
        except Exception as e:
            logger.error("set_bg error: {e}")

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)