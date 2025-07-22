# stories/urls.py
from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    path("create/", views.story_create, name="create"),
    path('view/<int:user_id>/', views.story_view, name='view'),
    path('stories/<int:story_id>/delete_ajax/', views.story_delete_ajax, name='story_delete_ajax'),
]