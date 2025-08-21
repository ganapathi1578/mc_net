from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "is_published")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "body", "author__email", "author__name")
