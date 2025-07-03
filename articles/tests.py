from django.test import TestCase
from django.contrib.auth.models import User
from articles.models import Article
from django.core.exceptions import ValidationError


class ArticleModelTest(TestCase):
    
    def test_article_creation_with_title(self):
        user = User.objects.create_user(username='testuser', password='password123')
        article = Article.objects.create(title="テスト記事", body="これは本文です", author=user)
        self.assertEqual(article.title, "テスト記事")
        self.assertEqual(article.author.username, "testuser")

    def test_slug_is_generated(self):
        user = User.objects.create_user(username='sluguser', password='test')
        article = Article.objects.create(title="こんにちは世界", body="これはテスト記事です。", author=user)
        self.assertTrue(article.slug)  # 空でないことを確認

    def test_article_without_body_fails(self):
        user = User.objects.create_user(username='failuser', password='test')
        article = Article(title="タイトルのみ", author=user, body="")
        with self.assertRaises(ValidationError):
            article.full_clean()
            article.save()

    def test_like_counting(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        article = Article.objects.create(title="like test", body="test", author=user1)
        article.like.add(user2)
        self.assertEqual(article.total_likes, 1)