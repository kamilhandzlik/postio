from django import forms
from .models import UserPackage
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class UserPackageForm(forms.ModelForm):
    class Meta:
        model = UserPackage
        fields = ['name', 'weight', 'width', 'lenght', 'height']
        labels = {
            'name': 'Nazwa',
            'weight': 'Waga (max 15 kg)',
            'width': 'Szerokość (max 30 cm)',
            'lenght': 'Długość (max 45 cm)',
            'height': 'Wysokość (max 35 cm)',
            'assigned_courier': 'Przypisany kurier',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'lenght': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'assigned_courier': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        lenght = cleaned_data.get('lenght')

        if weight > 15:
            self.add_error('weight', 'Waga paczki nie może przekraczać 15 kg.')
        if width > 30:
            self.add_error('width', 'Szerokość paczki nie może przekraczać 30 cm.')
        if height > 35:
            self.add_error('height', 'Wysokość paczki nie może przekraczać 35 cm.')
        if lenght > 45:
            self.add_error('lenght', 'Długość paczki nie może przekroczyć 45 cm.')

        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['address']

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Stare hasło'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        error_messages={
            'required': _('To pole jest wymagane.'),
        }
    )
    new_password1 = forms.CharField(
        label=_('Nowe hasło'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=_("Twoje hasło nie może być podobne do twoich innych danych osobowych. "
                    "Twoje hasło musi zawierać co najmniej 8 znaków. "
                    "Twoje hasło nie może być powszechnie używane. "
                    "Twoje hasło nie może składać się wyłącznie z cyfr."),
        error_messages={
            'required': _('To pole jest wymagane.'),
        }
    )
    new_password2 = forms.CharField(
        label=_('Potwierdź nowe hasło'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=_("Wprowadź to samo hasło, co powyżej, w celu weryfikacji."),
        error_messages={
            'required': _('To pole jest wymagane.'),
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update({
            'password_mismatch': _('Hasła nie pasują do siebie.'),
            'password_incorrect': _('Stare hasło jest niepoprawne.')
        })

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
