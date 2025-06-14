from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.files import File

import os
import pillow_heif
pillow_heif.register_heif_opener()

from PIL import Image, ImageOps, ExifTags
from io import BytesIO


class Article(models.Model):
    title      = models.CharField(max_length=30)
    slug       = models.SlugField()
    body       = models.TextField('Article', blank=False, help_text='')
    date       = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    thumb      = models.ImageField('Photo', default='No-image.png', blank=True, upload_to='article_pics')
    category   = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, blank=True)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    like       = models.ManyToManyField(User, related_name="likes", blank=True)
    book_mark  = models.ManyToManyField(User, related_name='book_mark', blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:46] + '...'

    def get_user(self):
        return self.author

    def get_url(self):
        return reverse('articles:detail', kwargs={'detail_id': self.id})

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
        print("save called")
        self.set_image()  # 画像処理とファイル名変更を常に実行
        super().save(*args, **kwargs)

    # ...existing code...
    def set_image(self):
        try:
            if not self.thumb:
                return
            if self.thumb == 'No-image.png':
                return
            self.thumb.seek(0)
            # ...existing code...
            pil_image = Image.open(BytesIO(self.thumb.read()))

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
            # ...リサイズ・保存処理...

            # リサイズ
            if pil_image.height > 598 or pil_image.width > 598:
                size      = (598, 598)
                pil_image = ImageOps.fit(pil_image, size, Image.Resampling.LANCZOS)


            # ...existing code...
            output = BytesIO()
            pil_image.save(output, format="JPEG", quality=70, optimize=True)
            output.seek(0)

            # ファイル名を明示的にjpgに
            base     = os.path.splitext(self.thumb.name)[0]
            filename = base + ".jpg"
            self.thumb.delete(save=False)  # 古いファイルを削除
            self.thumb.save(filename, File(output), save=False)
            # ...existing code...

        except Exception as e:
            print("set_image error:", e)
            pass
    # ...existing code...


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
