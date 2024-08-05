from django import forms
from .models import UserPackage
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from register.models import Profile


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
