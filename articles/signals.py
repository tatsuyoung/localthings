from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    if instance.author == instance.post.get_user():
        recipient = instance.post.get_user()
        verb = f'Responded to {instance.post}'
    else:
        recipient = instance.post.get_user()
        verb = f'Commented on your {instance.post}'
    url = instance.post.get_url()
    notify.send(instance.author, recipient=recipient, verb=verb, action_object=instance, url=url)