from django import forms
from .models import Task

class FilterForm(forms.Form):
    category = forms.CharField(max_length=100)

