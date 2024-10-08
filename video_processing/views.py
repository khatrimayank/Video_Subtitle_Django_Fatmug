from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video, Subtitle  # Ensure Subtitle is imported
from .tasks import extract_subtitles
from django.http import Http404  # Import Http404


def upload_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            subtitles = extract_subtitles(
                video.id
            )  # Ensure this function is working properly
            video.subtitles = subtitles  # Save the extracted subtitles
            video.save()  # Save the video instance again
            return redirect("video_list")
    else:
        form = VideoForm()
    return render(request, "video_processing/upload.html", {"form": form})


def video_list(request):
    videos = Video.objects.prefetch_related("subtitle_set").all()
    return render(request, "video_processing/list.html", {"videos": videos})


def search_subtitles(request, video_id):
    query = request.GET.get("q", "").lower()
    language = request.GET.get("lang", "en")  # Default to English
    subtitles = Subtitle.objects.filter(video_id=video_id, language=language)
    results = []

    for subtitle in subtitles:
        if query in subtitle.text.lower():
            results.append(subtitle)

    return render(
        request,
        "video_processing/search_results.html",
        {
            "results": results,
            "video": Video.objects.get(id=video_id),
            "selected_language": language,
        },
    )


def index(request):
    return render(request, "video_processing/index.html")
