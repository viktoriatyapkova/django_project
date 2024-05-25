from django import forms
from django.contrib.auth import forms, models
from django.utils.translation import gettext_lazy as _

class Registration(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']