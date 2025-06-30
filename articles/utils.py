def format_custom_date_style(date, now):
    delta = now - date
    if delta.days < 7:
        return f"{delta.days}日前" if delta.days > 0 else "今日"
    else:
        return date.strftime("%-m月%-d日")  # Linux/Mac
        # return date.strftime("%#m月%#d日")  # Windowsの場合