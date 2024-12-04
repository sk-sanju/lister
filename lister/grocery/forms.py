from django import forms
from .models import GroceryItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class GroceryItemForm(forms.ModelForm):
    class Meta:
        model = GroceryItem
        fields = ['category', 'name', 'quantity', 'photo']
