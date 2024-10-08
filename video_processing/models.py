# videos/models.py

from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="videos/")
    subtitles = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()  # Make sure this matches the field you're using
    start_time = models.FloatField()  # Ensure you have the correct field names
    end_time = models.FloatField()  # If this is in use
    language = models.CharField(max_length=10, default="en")

    def __str__(self):
        return self.text
