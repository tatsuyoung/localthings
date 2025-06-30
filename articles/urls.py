from django.urls import path
from articles import views
from .views import UserPostListView, Gallery, ArticleOrderedByLikes


app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name="list"),
    path('<int:pk>/comment/', views.article_comment, name="comment_post"),
    path('create/', views.article_create, name="create"),
    path('<int:pk>/', views.article_detail, name="detail"),
    path('<int:article_id>/delete', views.article_delete, name="delete"),
    path('<int:comment_id>/ajax_delete/', views.delete_comment_ajax, name='comment_ajax_delete'),
    path('<int:like_id>/like/', views.like_button, name='like_button'),
    path('<int:book_mark_id>/book_mark/', views.book_mark, name='book_mark'),
    path('<int:pk>/user_detail', views.users_detail, name='users_detail'),
    path('<int:pk>/user_detail_comments', views.users_detail_comments, name='users_detail_comments'),
    path('<int:pk>/user_detail_like', views.users_detail_liked, name='users_detail_like'),
    path('<int:pk>/edit/', views.article_edit, name='edit'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('galley/', Gallery.as_view(), name='gallery'),
    path('ordered_by_likes/', ArticleOrderedByLikes.as_view(), name='ordered_by_likes'),
    path('my_book_mark_list/', views.book_mark_list, name='book_mark_list'),
    path('<int:pk>/category', views.category_detail, name='category_detail'),
]