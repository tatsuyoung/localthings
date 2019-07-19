# Generated by Django 2.1.7 on 2019-05-10 07:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0011_auto_20190508_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='like',
        ),
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
