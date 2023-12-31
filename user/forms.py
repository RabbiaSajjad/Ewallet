# your_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'full_name', 'cnic', 'address', 'contact', 'profile_picture']

class UserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'full_name', 'cnic', 'address', 'contact', 'profile_picture']
