from django.urls import path

from accounts.views import ProfileDetailView, UserFollowingFeedView
from.import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('contact/', views.Contact, name="contact"),
    path('success/', views.Success, name="success"),
    path('profile', views.profile, name="profile"),
    path('unsubscribe', views.Delete_user, name="unsubscribe"),
    path('<str:username>', ProfileDetailView.as_view(), name='profile_detail'),
    path('user_following/', UserFollowingFeedView.as_view(), name='user_following'),
    path('<str:username>/is_following', views.user_is_following, name='is_following'),
    path('<str:username>/followers', views.user_followers, name='followers'),
    ]