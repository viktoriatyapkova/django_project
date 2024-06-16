"""Module with forms."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from python_project_app.models import Client, Shop


class Registration(UserCreationForm):
    """User registration form using the built-in UserCreationForm form."""

    class Meta:
        """A metaclass that defines the metadata of the registration form."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddShopForm(forms.Form):
    """Form for adding a store. Uses ModelChoiceField to select a specific store."""

    shop = forms.ModelChoiceField(queryset=Shop.objects.all())


class ProfilePhotoForm(forms.ModelForm):
    """A form for uploading a client profile photo."""

    class Meta:
        """A metaclass that defines the metadata of the profile photo upload form."""

        model = Client
        fields = ('photo',)
