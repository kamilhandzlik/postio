from .forms import RegistrationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserForm, PasswordChangeCustomForm


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
    next_page = reverse_lazy('homepage')



class ProfileView(LoginRequiredMixin, View):
    template_name = 'main/profile.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user)

        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)

        if 'username' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profil został zaktualizowany pomyślnie.')
                return redirect('profile')

        if 'old_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Hasło zostało zmienione pomyślnie.')
                return redirect('profile')
            else:
                messages.error(request, "Wystąpił błąd. Proszę spróbuj ponownie.")

        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })


class PasswordChangeAjaxView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'status': 'ok'}, status=200)
            #         else:
            return JsonResponse({'status': 'error', 'errors': 'form.errors'}, status=400)
