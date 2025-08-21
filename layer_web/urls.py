from django.contrib import admin
from django.urls import path
from .views import (
    send_test_mail
)
urlpatterns = [
    path('send', send_test_mail),
]
