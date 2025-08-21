from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import EmailVerification, Profile

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_active", "is_staff")
    search_fields = ("email", "name")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at")
