from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from accounts.views import ProfileFollowToggle
from articles import views as article_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from trydjango.sitemaps import ArticleSitemap, StaticSitemap
from.import views

sitemaps = {
    'articles': ArticleSitemap,
    'static': StaticSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', views.about, name="about"),
    path('', article_views.article_list, name="home"),
    path('special_thanks/', views.homepage, name="special_thanks"),
    path('privacy-policy', views.privacy_policy, name="privacy-policy"),
    path('sw.js', (TemplateView.as_view(template_name="sw.js",
                                        content_type='application/javascript',)), name='sw.js'),
    path('profile-follow/', ProfileFollowToggle.as_view(), name='follow'),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('my_notifications/', views.my_notifications, name='my_notifications'),
    path('my_notification/<int:my_notification_pk>', views.my_notification, name='my_notification'),
    path('delete_my_read_notifications/', views.delete_my_read_notifications, name='delete_my_read_notifications'),
    path('oauth/', include('social_django.urls', namespace='social')),
    ]

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)