# 🌏 Local Things

**Local Things**は、あなたの「地元愛」を世界に広げるためのご当地SNSです。  
「地元の魅力をもっと発信したい」「地域の人とつながりたい」そんな想いを持つあなたと一緒に、面白いことを作っていきたいです！

---

## 🚀 主な機能

- **ログイン／ログアウト・新規登録**  
  いいね・コメント・プロフィール作成や編集、記事投稿などが可能に！

- **記事投稿・編集・削除**  
  写真付きの記事を簡単に投稿。画像は自動リサイズで安心。

- **コメント・いいね・ブックマーク**  
  気になる記事にリアクション＆お気に入り保存。

- **ユーザーページ・プロフィール編集**  
  あなたの投稿やプロフィールを自由にカスタマイズ。

- **通知機能**  
  コメントやいいねが届くと、ベルアイコンにバッジでお知らせ！

- **フォロー・フォロワー機能**  
  気になるユーザーをフォローして、タイムラインをもっと楽しく。

- **ギャラリー・検索・カテゴリー別表示**  
  写真一覧やカテゴリーごとの記事閲覧も簡単。

- **SNS連携・Twitterカード**  
  TwitterやFacebookと連携、シェアもスムーズ。

- **PWA対応**  
  スマホのホーム画面からアプリのように使えます。

- **セキュリティ対策**  
  403/404/500のカスタムエラーページや、各種セキュリティ設定も万全。

- **進捗バー（アップロード時）**  
  S3/Heroku環境ではダミーアニメーションで楽しく演出！

- **その他にも…**  
  パスワードリセット、サイトマップ、通知、ブックマーク、記事の並び替え、背景変更など盛りだくさん！

---

## 🛠️ 技術スタック

- **言語**: Python 3.11.9, HTML5, CSS3, JavaScript, jQuery, Ajax
- **フレームワーク**: Django 3.2.25
- **本番環境**: Heroku, AWS S3

---

## 💡 こんな方におすすめ

- 地域の魅力を発信したい
- 地元の人とつながりたい
- 新しいSNSを体験したい
- コミュニティを盛り上げたい

---

## 📱 SNS

- [X (Twitter)](https://twitter.com/tatsuyoung55)

---

**あなたの地元も、Local Thingsで盛り上げよう！**

# 🌏 Local Things (English)

**Local Things** is a local SNS to spread your love for your hometown to the world.  
If you want to share the charm of your region or connect with local people, join us and make something fun together!

---

## 🚀 Main Features

- **Login / Logout / Register**  
  Like, comment, create or edit your profile, and post articles!

- **Post, Edit, and Delete Articles**  
  Easily post articles with photos. Images are automatically resized for your convenience.

- **Comments, Likes, and Bookmarks**  
  React to posts and save your favorites.

- **User Pages & Profile Editing**  
  Customize your posts and profile freely.

- **Notification System**  
  Get notified with a badge when you receive comments or likes!

- **Follow & Follower System**  
  Follow users you’re interested in and enjoy a more personalized timeline.

- **Gallery, Search, and Category Views**  
  Browse photos and articles by category with ease.

- **SNS Integration & Twitter Cards**  
  Share easily with Twitter and Facebook.

- **PWA Support**  
  Use it like an app from your smartphone’s home screen.

- **Security**  
  Custom error pages (403/404/500) and robust security settings.

- **Progress Bar (Upload)**  
  Fun dummy animation for uploads on S3/Heroku environments!

- **And much more...**  
  Password reset, sitemap, notifications, bookmarks, article sorting, background changes, and more!

---

## 🛠️ Tech Stack

- **Languages**: Python 3.11.9, HTML5, CSS3, JavaScript, jQuery, Ajax
- **Framework**: Django 3.2.25
- **Production**: Heroku, AWS S3

---
### 以下の環境変数を .env ファイルに設定してください（本番用/開発用に応じて値を変更してください）：

### Please set the following environment variables in your .env file. Adjust the values depending on whether you’re in production or development.

# デバッグモードの有効化（Trueで有効）  
# Enable debug mode (True = ON)
DEBUG=True

# 環境種別（例: production, development）  
# Environment type (e.g., production, development)
ENV=production

# Django のシークレットキー  
# Django secret key
SECRET_KEY=your-django-secret-key

# メール送信に使用する Gmail アドレス  
# Gmail address used for sending emails
EMAIL_HOST_USER=your-email@example.com

# 上記メールアドレスの「アプリパスワード」  
# App password for the above email (not your regular password)
EMAIL_HOST_PASSWORD=your-app-password

# AWS アクセスキー（S3に使用）  
# AWS access key (for S3)
AWS_ACCESS_KEY_ID=your-aws-access-key

# AWS シークレットキー  
# AWS secret key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key

# アップロード先のS3バケット名  
# S3 bucket name for file uploads
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name

# データベース接続URL（例: PostgreSQL）  
# Database connection URL (e.g., PostgreSQL)
DATABASE_URL=postgres://user:password@hostname:5432/dbname

# Google OAuth クライアントID  
# Google OAuth client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id

# Google OAuth クライアントシークレット  
# Google OAuth client secret
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret

# Twitter APIキー  
# Twitter API key
SOCIAL_AUTH_TWITTER_KEY=your-twitter-key

# Twitter APIシークレット  
# Twitter API secret
SOCIAL_AUTH_TWITTER_SECRET=your-twitter-secret

## 📄 環境変数の設定 (.envファイル)

このリポジトリには `.env.example` が含まれています。以下のコマンドでコピーし、必要な値を入力してください：
The .env.example file is included in this repository. Copy it and edit the values as needed:

```bash
cp .env.example .env