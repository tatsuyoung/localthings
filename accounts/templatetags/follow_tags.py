# accounts/templatetags/follow_tags.py
from django import template

register = template.Library()

@register.simple_tag
@register.simple_tag
def mutual_follow_status(current_user, target_user):
    if not current_user.is_authenticated:
        return ""

    # current_user がフォローしているユーザーの username を取得（Profile → User 経由）
    following_usernames = set(p.user.username for p in current_user.following_users.all())

    # target_user がフォローしているユーザーの username を取得
    target_following_usernames = set(p.user.username for p in target_user.following_users.all())

    is_following = target_user.username in following_usernames
    is_followed_by = current_user.username in target_following_usernames

    if is_following and is_followed_by:
        return "相互フォロー中です"
    elif is_following:
        return "フォロー中です"
    elif is_followed_by:
        return "フォローされています"
    return ""