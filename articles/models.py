from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from PIL import ImageOps
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File


class Article(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()
    body = models.TextField('Article', blank=False, help_text='Titleまたは、Articleに地域名等を入れると検索し易くなります。')
    date = models.DateTimeField(default=timezone.now)
    thumb = models.ImageField('Photo', default='No-image.png', blank=True, upload_to='article_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + '...'

    def get_user(self):
        return self.author

    def get_url(self):
        return reverse('articles:detail', kwargs={'detail_id': self.id})

    @property
    def total_likes(self):
        return self.like.count()

    @property
    def get_counter(self):
        return Article.objects.count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if not self.id:
            self.set_image()
        else:
            this = Article.objects.get(id=self.id)
            if this.thumb != self.thumb:
                self.set_image()
        return super(Article, self).save(*args, **kwargs)

    def set_image(self):
        try:
            if self.thumb:
                pilImage = Img.open(BytesIO(self.thumb.read()))
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                if pilImage.height > 728 or pilImage.width > 728:
                    size = (728, 728)
                    pilImage_fit = ImageOps.fit(pilImage, size, Img.ANTIALIAS)
                    pilImage_fit.save(output, format='JPEG', quality=70)
                    output.seek(0)
                    self.thumb = File(output, self.thumb.name)
                    self.slug = slugify(self.title)
                else:
                    pilImage.save(output, format='JPEG', quality=66)
                    output.seek(0)
                    self.thumb = File(output, self.thumb.name)
                    self.slug = slugify(self.title)
        except(AttributeError, KeyError, IndexError):
            pass


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField(help_text='コメントを送信する場合は、Comments横のIcon(吹き出しマーク)をTapして下さい')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return "{} - {}".format(str(self.author.username), str(self.post.title))
