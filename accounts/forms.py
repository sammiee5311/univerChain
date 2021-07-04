from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)

from .models import myuser


class RegisterationForm(forms.ModelForm):
    username = forms.CharField(label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Please, type a valid email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)
    ethereum_account = forms.CharField(label='Ethereum Account', max_length=512, help_text='Required')

    class Meta:
        model = myuser
        fields = ('username', 'email',)

    def clean_username(self):
        cleaned_name = self.cleaned_data['username'].lower()
        duplication = myuser.objects.filter(username=cleaned_name)

        if duplication.count():
            raise forms.ValidationError('Username already exists')

        return cleaned_name

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['password'] != cleaned_data['password_confirm']:
            raise forms.ValidationError('Passwords do not macth')

        return cleaned_data['password_confirm']

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        duplication = myuser.objects.filter(email=cleaned_email)

        if duplication.exists():
            raise forms.ValidationError('Email already exists')

        return cleaned_email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password_confirm'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password Confirmation'})
        self.fields['ethereum_account'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Account of Ethereum'})