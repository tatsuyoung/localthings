from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File


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
        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pics',
                              help_text='著作権があるものはiconにはできません。')
    bio = models.TextField(max_length=160, blank=True, null=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if not self.id:
            self.set_image()
        else:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image:
                self.set_image()
        return super(Profile, self).save(*args, **kwargs)

    def set_image(self):
        try:
            if self.image:
                pilImage = Img.open(BytesIO(self.image.read()))
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                e = pilImage._getexif()
                if e is not None:
                    exif = dict(e.items())
                    if exif[orientation] == 3:
                        pilImage = pilImage.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        pilImage = pilImage.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        pilImage = pilImage.rotate(90, expand=True)

                    output = BytesIO()
                    if pilImage.height > 192 or pilImage.width > 192:
                        size = (192, 192)
                        pilImage_fit = ImageOps.fit(pilImage, size, Img.ANTIALIAS)
                        pilImage_fit.save(output, format='JPEG', quality=70)
                        output.seek(0)
                        self.image = File(output, self.image.name)
                    else:
                        pilImage.save(output, format='JPEG', quality=90)
                        output.seek(0)
                        self.image = File(output, self.image.name)
                elif e is None:
                    output = BytesIO()
                    if pilImage.height > 192 or pilImage.width > 192:
                        size = (192, 192)
                        pilImage_fit = ImageOps.fit(pilImage, size, Img.ANTIALIAS)
                        pilImage_fit.save(output, format='JPEG', quality=70)
                        output.seek(0)
                        self.image = File(output, self.image.name)
                    else:
                        pilImage.save(output, format='JPEG', quality=90)
                        output.seek(0)
                        self.image = File(output, self.image.name)
        except(AttributeError, KeyError, IndexError):
            pass

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)