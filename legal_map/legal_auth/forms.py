from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

UserModel = get_user_model()


class SignInForm(AuthenticationForm):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)
