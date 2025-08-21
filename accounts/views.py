from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import EmailVerification, Profile
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # basic validation
        if not (name and email and password):
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login or use another email.")
            return render(request, "accounts/register.html")

        # create inactive user
        user = User.objects.create_user(email=email, name=name, password=password)
        user.is_active = False
        user.save()

        # create verification code (UUID) record
        verification = EmailVerification.objects.create(user=user)

        # send email (uses DEFAULT_FROM_EMAIL from settings)
        send_mail(
            subject="Verify your NITMZ Society account",
            message=(
                f"Hello {name},\n\n"
                f"Thank you for registering. Use the following code to verify your account:\n\n"
                f"{verification.code}\n\n"
                f"If you did not register, ignore this email."
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER),
            recipient_list=[email],
            fail_silently=False,
        )

        # tell user to check mail and show a page with instructions
        return render(request, "accounts/check_email.html", {"email": email})

    return render(request, "accounts/register.html")


def verify(request):
    """
    User posts a code. If code valid -> activate user, create profile, login redirect to profile.
    """
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        if not code:
            messages.error(request, "Please enter the verification code.")
            return render(request, "accounts/verify.html")

        try:
            verification = EmailVerification.objects.get(code=code)
        except EmailVerification.DoesNotExist:
            messages.error(request, "Invalid or expired verification code.")
            return render(request, "accounts/verify.html")

        user = verification.user
        user.is_active = True
        user.save()

        # create profile if not exists
        Profile.objects.get_or_create(user=user)

        # delete verification record (one-time)
        verification.delete()

        messages.success(request, "Email verified successfully. Please login.")
        return redirect("accounts:login")

    # GET
    return render(request, "accounts/verify.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        if not (email and password):
            messages.error(request, "Both email and password are required.")
            return render(request, "accounts/login.html")

        # authenticate — your CustomUser must have USERNAME_FIELD='email'
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("accounts:profile")
            else:
                messages.error(request, "Account not verified. Please check your email.")
                return redirect("accounts:verify")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


def profile(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # safe get_or_create profile (should exist after verification)
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile_obj})


@login_required
def edit_profile(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if uform.is_valid() and pform.is_valid():
            u = uform.save(commit=False)
            u.email = request.user.email
            u.save()
            pform.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        uform = UserUpdateForm(instance=user)
        pform = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"uform": uform, "pform": pform})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        # let the built-in view save the new password and get its response
        response = super().form_valid(form)

        # ensure session keeps the user authenticated with new password
        update_session_auth_hash(self.request, self.request.user)

        # send notification email (no password included)
        try:
            user = self.request.user
            send_mail(
                subject="Your NITMZ Society account password changed",
                message=(
                    f"Hello {getattr(user, 'name', user.email)},\n\n"
                    "This is a confirmation that your account password was successfully changed.\n\n"
                    "If you did not change your password, please contact support immediately or reset your password."
                ),
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER),
                recipient_list=[user.email],
                fail_silently=True,   # avoid breaking UX if email fails
            )
        except Exception:
            # fail silently in production; you can log the exception if desired
            pass

        return response


# PasswordChangeDoneView (optional custom template)
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"