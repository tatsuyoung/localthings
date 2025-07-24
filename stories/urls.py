# stories/urls.py
from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    path("create/", views.story_create, name="create"),
    path('stories/<int:story_id>/delete_ajax/', views.story_delete_ajax, name='story_delete_ajax'),
    path('view/<int:user_id>/', views.story_view, name='view'),
    path("mark_read/<int:story_id>/", views.mark_story_read, name="mark_story_read"),
]