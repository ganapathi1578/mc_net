from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "body", "image", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "body": forms.Textarea(attrs={"class":"form-control", "rows":4}),
        }
