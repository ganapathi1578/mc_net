from django.shortcuts import render, HttpResponse

# Create your views here.
from django.core.mail import send_mail

def send_test_mail(request):
    print('Request came', flush=True)
    send_mail(
        subject="Hello from NITMZ Mail",
        message="This is a test email using institute email.",
        from_email="bt23ma005@nitmz.ac.in",
        recipient_list=["ganapathi1578@gmail.com"],
        fail_silently=False,
    )
    print('request completed', flush=True)
    return HttpResponse("✅ Email sent successfully!")
