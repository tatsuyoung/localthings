from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from notifications.models import Notification


def homepage(request):
    return render(request, 'special_thanks.html')


def about(request):
    return render(request, 'about.html')


def privacy_policy(request):
    return render(request, 'privacy-policy.html')


def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)


def my_notification(request, my_notification_pk):
    my_notify = get_object_or_404(Notification, pk=my_notification_pk)
    my_notify.unread = False
    my_notify.save()
    return redirect(my_notify.data['url'])


def delete_my_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))