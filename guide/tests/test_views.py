from django.test import TestCase, Client
from django.urls import reverse
import simplejson

class HomeTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/guide/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class MyTripPlanListViewTest(TestCase):

    def setUp(self):
        self.client = Client()

