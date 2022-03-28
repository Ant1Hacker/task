from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import User, Link, EducationAndEmploymentHistory
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'region', 'profile', 'languages')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            user_cache = authenticate(username=username, password=password)
            if user_cache is None:
                raise ValidationError(
                    'Wrong credentials ',
                    code="bad_credentials",
                )
            else:
                return self.cleaned_data


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('type', 'link')


class EducationAndEmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EducationAndEmploymentHistory
        fields = ('type', 'title', 'description')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'region', 'address', 'profile',
            'place_of_birth', 'skills', 'hobbies', 'languages', 'achievements'
        )
