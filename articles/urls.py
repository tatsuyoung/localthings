from django.urls import path
from articles import views
from .views import UserPostListView, AuthorProfileView

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name="list"),
    path('create/', views.article_create, name="create"),
    path('<int:detail_id>/', views.article_detail, name="detail"),
    path('<int:article_id>/delete', views.article_delete, name="delete"),
    path('<int:pk>/comment/', views.article_comment, name="comment"),
    path('<int:comment_id>/delete_comment', views.delete_comment, name="com_delete"),
    path('<int:like_id>/like/', views.like_button, name='like_button'),
    path('<int:pk>/user_detail', views.users_detail, name='users_detail'),
    path('<int:pk>/user_detail_comments', views.users_detail_comments, name='users_detail_comments'),
    path('<int:pk>/user_detail_like', views.users_detail_liked, name='users_detail_like'),
    path('<int:pk>/edit/', views.article_edit, name='edit'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('author/<str:username>', AuthorProfileView.as_view(), name='author-view'),
]