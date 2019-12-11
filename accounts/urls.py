from django.urls import path
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
    ]