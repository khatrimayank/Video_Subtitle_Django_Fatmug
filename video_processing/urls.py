from django.urls import path
from . import views  # Import the views from the current app
from .views import upload_video, video_list, index

urlpatterns = [
    path("", index, name="index"),  # Home page
    path("upload/", upload_video, name="upload_video"),  # Video upload page
    path("videos/", video_list, name="video_list"),  # Video list page
    path("search/<int:video_id>/", views.search_subtitles, name="search"),
]
