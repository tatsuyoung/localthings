from django.urls import path

from accounts.views import ProfileDetailView, UserFollowingFeedView
from.import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('contact/', views.Contact, name="contact"),
    path('success/', views.Success, name="success"),
    path('profile', views.profile, name="profile"),
    path('unsubscribe', views.Delete_user, name="unsubscribe"),
    path('<str:username>', ProfileDetailView.as_view(), name='profile_detail'),
    path('user_following/', UserFollowingFeedView.as_view(), name='user_following'),
    ]