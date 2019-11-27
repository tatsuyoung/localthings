from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from articles import views as article_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin, sitemaps
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views

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
    path('about/', views.about, name="about"),
    path('', article_views.article_list, name="home"),
    path('homepage/', views.homepage),
    path('privacy-policy', views.privacy_policy, name="privacy-policy"),
    path('accounts/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('accounts/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('accounts/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('sw.js', (TemplateView.as_view(template_name="sw.js",
                                        content_type='application/javascript',)), name='sw.js'),
    ]

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)