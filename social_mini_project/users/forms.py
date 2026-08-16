from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationProfileForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже зарегистрирован.")
        return email

    def clean_username(self):
            username = self.cleaned_data["username"]
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError("Такой username уже зарегистрирован.")
            return username


class EditingProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, validators=[CustomUser.validate_file_size])

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "avatar", "bio", "date_of_birth")
