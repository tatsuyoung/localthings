from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, created, **kwargs):
    # 新しく作成されたときのみ通知を送る
    if not created:
        return

    post_user      = instance.post.get_user()
    comment_author = instance.author

    # 自分の投稿に自分でコメントした場合は通知しない
    if comment_author == post_user:
        return

    # 通知対象者を変更する: 親コメントの投稿者に通知する
    if instance.is_reply():
        parent_author = instance.parent.author
        # 自分自身への返信は通知不要
        if comment_author == parent_author:
            return
        recipient = parent_author
        verb = f'さんが、あなたのコメントに返信しました: {instance.post}'
    else:
        recipient = post_user
        verb = f'さんが、あなたの投稿にコメントしました: {instance.post}'

    # 通知送信
    notify.send(
        sender=comment_author,
        recipient=recipient,
        verb=verb,
        action_object=instance,
        url=instance.post.get_url()
    )