from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    body = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='no-image.png', blank=True, upload_to='article_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    like = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + '...'

    @property
    def total_likes(self):
        return self.like.count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField(help_text='コメントを送信する場合は、Comments横のIconをTapして下さい')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return "{} - {}".format(str(self.author.username), str(self.post.title))
