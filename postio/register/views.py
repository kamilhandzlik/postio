from .forms import RegistrationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.register.html'
    success_url = reverse_lazy('homepage')


class CustomLoginView(LoginView):
    template_name = 'register.login.html'
    success_url = reverse_lazy('homepage')


class CustomLogoutView(LogoutView):
    pass
