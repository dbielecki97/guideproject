from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='Nazwa planu', max_length=150)


class SignUpForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

""" @override save func from UserCreationForm
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user """