from django import forms
from .models import UserPackage


class UserPackageForm(forms.ModelForm):
    class Meta:
        model = UserPackage
        fields = ['name', 'weight', 'width', 'lenght', 'height']

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
