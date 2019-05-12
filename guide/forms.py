from django import forms
from guide.models import Client, Attraction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='Nazwa planu', max_length=150)


class ChangeTripPlanNameForm(forms.Form):
    name = forms.CharField(label='Nowa nazwa planu', max_length=150)


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs = {'style': 'width: 100%'}
        self.fields['email'].widget.attrs = {'style': 'width: 100%'}
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs = {'style': 'width: 100%'}
        self.fields['password2'].widget.attrs = {'style': 'width: 100%'}

    class Meta:
        model = Client
        fields = ("username", 'email', "password1", "password2")    

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
            super(PasswordChangeForm, self).__init__(*args, **kwargs)
            for key in self.fields:
                self.fields[key].widget.attrs = {'style' : 'width: 40%'}


class CustomUserChangeForm(UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
            super(CustomUserChangeForm, self).__init__(*args, **kwargs)
            self.fields['email'].required = True
            for key in self.fields:
                self.fields[key].widget.attrs = {'style' : 'width: 40%'}
            
    class Meta:
        model = Client
        fields =('email', 'name', 'surname')
    
