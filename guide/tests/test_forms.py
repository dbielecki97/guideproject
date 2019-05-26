from django.test import TestCase

from guide.forms import SaveTripPlanForm
from guide.forms import ChangeTripPlanNameForm

class SaveTripPlanFormTest(TestCase):
    def test_name_field_label(self):
        form = SaveTripPlanForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == '')

class ChangeTripPlanNameFormTest(TestCase):
    def test_name_field_label(self):
        form = ChangeTripPlanNameForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == '')
    