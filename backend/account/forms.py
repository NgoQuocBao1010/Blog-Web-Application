from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "avatar",
            "twitter",
            "instagram",
            "youtube",
        ]
