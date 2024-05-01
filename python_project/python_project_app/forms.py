from django import forms

class MyForm(forms.Form):
    my_field = forms.FloatField(widget=forms.NumberInput(attrs={'min': 0, 'max': 5}))
