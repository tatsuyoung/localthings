from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from articles.models import Article


class ArticleSitemap(Sitemap):
    changfreq = "never"
    priotity = 0.5

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return reverse('articles:detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.date


class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ['home',
                'about',
                'privacy-policy'
                ]

    def location(self, item):
        return reverse(item)