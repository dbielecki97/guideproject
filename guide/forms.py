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
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['email'].widget.attrs = {'class': 'form-control'}
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Client
        fields = ("username", 'email', "password1", "password2")


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs = {'class': 'form-control'}


class CustomUserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for key in self.fields:
            self.fields[key].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Client
        fields = ('email', 'name', 'surname')
