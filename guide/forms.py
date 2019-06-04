from django import forms
from guide.models import Client, Attraction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField


class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'podaj nazwę planu',
        }))


class ChangeTripPlanNameForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'nowa nazwa',
        }))


class SignUpForm(UserCreationForm):
    captcha = ReCaptchaField(error_messages={
        "captcha_invalid": "Błąd przy weryfikacji reCAPTCHA, spróbuj ponownie.",
        "captcha_error": "Błąd przy weryfikacji reCAPTCHA, spróbuj ponownie.",
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'nazwa użytkownika'}
        self.fields['email'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'email'}
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'hasło'}
        self.fields['password2'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'potwierdzenie hasła'}

    class Meta:
        model = Client
        fields = ("username", 'email', "password1", "password2", 'captcha')


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs = {'class': 'form-control'}
        self.fields['old_password'].label = 'Stare hasło'
        self.fields['new_password1'].label = 'Nowe hasło'
        self.fields['new_password2'].label = 'Potwierdzenie hasła'


class CustomUserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for key in self.fields:
            self.fields[key].widget.attrs = {'class': 'form-control'}
        self.fields['email'].label = 'email'
        self.fields['name'].label = 'imie'
        self.fields['surname'].label = 'nazwisko'

    class Meta:
        model = Client
        fields = ('email', 'name', 'surname')
