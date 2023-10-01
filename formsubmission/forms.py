from datetime import date
from django import forms
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name',
            'gender',
            'phone',
            'email',
            'address',
            'nationality',
            'date_of_birth',
            'education_background',
            'preferred_contact',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select custom-select2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.Select(attrs={'class': 'form-select custom-select2'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'education_background': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-select custom-select2'}),
        }
        nationality = CountryField()

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['preferred_contact'].empty_label = None

    def clean_phone(self):
        """
        Custom validation for the phone field.
        Ensure that the phone number consists of digits only.
        """
        phone = self.cleaned_data['phone']
        if not phone.replace('-', '').isdigit():
            raise ValidationError("Invalid phone number. Use digits and dashes only.")
        return phone

    def clean_date_of_birth(self):
        """
        Custom validation for the date_of_birth field.
        Ensure that the date of birth is not in the future.
        """
        dob = self.cleaned_data['date_of_birth']
        if dob >= date.today():
            raise forms.ValidationError('Date of birth must be in the past')
        return dob
