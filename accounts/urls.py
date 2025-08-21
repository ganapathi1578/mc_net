from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("check-email/", lambda r: render(r, "accounts/check_email.html"), name="check_email"),  # optional direct page
    path("verify/", views.verify, name="verify"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path(
        "password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
