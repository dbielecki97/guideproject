from django import forms
from guide.models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='Nazwa planu', max_length=150)



class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].help_text = None
            self.fields['username'].help_text = None
            self.fields['username'].widget.attrs={'style': 'width: 100%'}
            self.fields['password1'].widget.attrs={'style': 'width: 100%'}
            self.fields['password2'].widget.attrs={'style': 'width: 100%'}

    class Meta:
        model = Client
        fields = ("username", "password1", "password2")    


    