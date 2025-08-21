from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),           # home / landing for events
    path("create/", views.event_create, name="create"),# create new event
    path("<int:pk>/", views.event_detail, name="detail"),
    path("<int:pk>/edit/", views.event_edit, name="edit"),       # <-- edit
    path("<int:pk>/delete/", views.event_delete, name="delete"), # 
]
