from django import forms
from guide.models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='Nazwa planu', max_length=150)


class SignUpForm(UserCreationForm):
    name = forms.CharField(label='Firstname',max_length=50)
    surname = forms.CharField(label='Surname', max_length=50)

    class Meta:
        model = Client
        fields = ("username", "name","surname", "password1", "password2")

        # @override save func from UserCreationForm
        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.name = self.cleaned_data["name"]
            user.surname = self.cleaned_data["surname"]
            if commit:
                user.save()
            return user 