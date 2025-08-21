from django.db import models
from django.conf import settings

class Event(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Describe the event (date, time, venue, details).")
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)  # use this to hide draft events if needed

    class Meta:
        ordering = ["-created_at"]  # latest first

    def __str__(self):
        return f"{self.title} ({self.author})"
