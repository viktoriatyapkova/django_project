from django import forms
from django.contrib.auth import forms, models
from django.utils.translation import gettext_lazy as _

# class MyForm(forms.Form):
#     my_field = forms.FloatField(widget=forms.NumberInput(attrs={'min': 0, 'max': 5}))

class Registration(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']