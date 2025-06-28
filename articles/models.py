from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.files import File

import re
from django.utils.text import slugify

import os
import pillow_heif
pillow_heif.register_heif_opener()

from PIL import Image, ImageOps, ExifTags
from io import BytesIO

import logging
logger = logging.getLogger(__name__)


class Article(models.Model):
    title      = models.CharField(max_length=30)
    slug       = models.SlugField(blank=True)
    body       = models.TextField('Article', blank=False, help_text='')
    date       = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    category   = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    like       = models.ManyToManyField(User, related_name="likes", blank=True)
    book_mark  = models.ManyToManyField(User, related_name='book_mark', blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:80].rsplit(' ', 1)[0] + '...'

    def get_user(self):
        return self.author

    def get_url(self):
        return reverse('articles:detail', kwargs={'pk': self.id})

    @property
    def total_likes(self):
        return self.like.count()

    @property
    def get_liked_user(self):
        return self.like.all()

    @property
    def get_counter(self):
        return Article.objects.count()

    def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None, *args, **kwargs):

        # body からタイトル自動生成（未入力時のみ）
        if not self.title:
            self.title = re.split(r'[。！？\n]', self.body)[0][:15] or 'Untitled'

        # slug 自動生成
        if not self.slug:
            self.slug = slugify(self.title)

        if not re.fullmatch(r'[a-zA-Z0-9-]+', self.slug):
            self.slug = '-'

        super().save(*args, **kwargs)


class ArticleImage(models.Model):
    article     = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField('Photo', default='No-image.png', blank=True, upload_to='article_pics')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {self.id}"
    # 画像処理はここに移動
    def save(self, num_image=5, *args, **kwargs):
        if self.article.images.count() >= num_image and not self.pk:
            raise ValueError(f"画像は最大{num_image}枚までしか追加できません。")
        self.process_image()
        super().save(*args, **kwargs)

    def process_image(self):
        try:
            if not self.image or self.image == 'No-image.png':
                return
            self.image.seek(0)
            pil_image = Image.open(BytesIO(self.image.read()))

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

            # 📐 Instagram用アスペクト比によるリサイズ処理
            original_width, original_height = pil_image.size
            aspect_ratio = original_width / original_height

            # Instagram Feed 用の推奨サイズに合わせる
            if aspect_ratio > 1.91:
                # 横長（e.g: 1080x566）
                target_size = (1080, int(1080 / 1.91))  # 約 1080x566
            elif aspect_ratio < 0.8:
                # 縦長（e.g: 1080x1350）
                target_size = (1080, 1350)
            else:
                # 正方形または近い(e.g: 1080x1080）
                target_size = (1080, 1080)

            pil_image = ImageOps.fit(pil_image, target_size, Image.Resampling.LANCZOS)

            # 最終保存処理
            output = BytesIO()
            pil_image.save(output, format="JPEG", quality=70, optimize=True)
            output.seek(0)

            # ファイル名を明示的にjpgに
            base     = os.path.splitext(self.image.name)[0]
            filename = base + ".jpg"
            self.image.delete(save=False)  # 古いファイルを削除
            self.image.save(filename, File(output), save=False)

        except Exception as e:
            logger.error(f"set_image error: {e}")

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    description   = models.CharField(max_length=50, 
    blank=True, null=True, default='No explanation')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'


class Comment(models.Model):
    post   = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name   = models.CharField(max_length=200)
    text   = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return "{} - {}".format(str(self.author.username), str(self.post.title))
