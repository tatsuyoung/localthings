# articles/templatetags/article_extras.py

import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def hashtag_links(text):
    # 正規表現で #タグ を見つけてリンクに置き換える
    def replace(match):
        tag = match.group(1)
        url = f"/articles/tags/{tag}/"
        return f'<a href="{url}" class="hashtag-link">#{tag}</a>'

    return mark_safe(re.sub(r"#(\w+)", replace, text))