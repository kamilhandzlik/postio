from .forms import RegistrationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register/register.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        # user_email = form.cleaned_data.get('email')
        # send_mail(
        #     "Rejestracja w serwisei Post-Io.",
        #     'Dziękujemy za rejestrację w naszym serwisie.',
        #     settings.EMAIL_HOST_USER,
        #     [user_email],
        #     fail_silently=False,
        # )
        return response



class CustomLoginView(LoginView):
    template_name = 'register/login.html'
    success_url = reverse_lazy('homepage')


class CustomLogoutView(LogoutView):
    pass
