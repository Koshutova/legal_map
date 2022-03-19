from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from legal_map.legal_auth.forms import SignUpForm, SignInForm

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'auth/sign-up.html'
    model = UserModel
    form_class = SignUpForm
    success_url = reverse_lazy('signin')


class SignInView(LoginView):
    template_name = 'auth/signin.html'
    form_class = SignInForm

    def get_success_url(self):
        return reverse('index')


def sign_out(request):
    logout(request)
    return redirect('index')