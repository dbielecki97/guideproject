from django import forms


class SaveTripPlanForm(forms.Form):
    name = forms.CharField(label='Nazwa planu', max_length=150)
