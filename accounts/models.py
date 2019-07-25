from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png',
                              upload_to='profile_pics',
                              help_text='著作権があるものはiconにはできません。')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
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
                exif = dict(pilImage._getexif().items())
                #print(exif)

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                pilImage.save(output, format='JPEG', quality=75)
                output.seek(0)
                self.image = File(output, self.image.name)
        except(AttributeError, KeyError, IndexError):
            pass