from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]            # allow editing name; optionally allow editing email
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "readonly": True}), 
            # readonly email to avoid extra verification complexity; remove readonly if you want editable email
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make email disabled in the form (non-editable)
        self.fields["email"].disabled = True

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
