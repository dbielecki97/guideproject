from django import forms
<<<<<<< HEAD
from guide.models import Client
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
=======
from guide.models import Client, Attraction
from django.contrib.auth.forms import UserCreationForm
>>>>>>> c757bf70e933ab581dc7ad7c0711008ce26145b2
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
        self.fields['password1'].widget.attrs = {'style': 'width: 100%'}
        self.fields['password2'].widget.attrs = {'style': 'width: 100%'}

    class Meta:
        model = Client
<<<<<<< HEAD
        fields = ("username", "password1", "password2")    


class CustomUserChangeForm(UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
            super(CustomUserChangeForm, self).__init__(*args, **kwargs)
            
    class Meta:
        model = Client
        fields =('email', 'name', 'surname')
    
=======
        fields = ("username", "password1", "password2")
>>>>>>> c757bf70e933ab581dc7ad7c0711008ce26145b2
