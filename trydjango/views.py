from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from notifications.models import Notification
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'special_thanks.html')


def about(request):
    return render(request, 'about.html')


def privacy_policy(request):
    return render(request, 'privacy-policy.html')

@login_required
def my_notifications(request):
    notifications = request.user.notifications.all()
    context = {'notifications': notifications}
    return render(request, 'my_notifications.html', context)


def my_notification(request, my_notification_pk):
    my_notify = get_object_or_404(Notification, pk=my_notification_pk)
    my_notify.unread = False
    my_notify.save()

    # 安全にURLを取得（dataがNoneの可能性がある）
    url = my_notify.data.get('url') if my_notify.data else None
    return redirect(url or '/')


def delete_my_read_notifications(request):
    request.user.notifications.read().delete()
    return redirect('my_notifications')