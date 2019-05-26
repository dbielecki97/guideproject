from django.test import TestCase
 
# Create your tests here.
 
 
from guide.models import Client
from guide.models import Category
from guide.models import Attraction
from guide.models import Localization
from guide.models import ShoppingCart
from guide.models import TripPlan

class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(name='Test client',surname='Testowy')

    def test_name_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name')

    def test_name_max_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_surname_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('surname').verbose_name
        self.assertEquals(field_label, 'Surname')

    def test_surname_max_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('surname').max_length
        self.assertEquals(max_length, 50)

    def test_object_label(self):
        client = Client.objects.get(id=1)
        object_label = client._meta.verbose_name
        self.assertEquals(object_label, 'client')

    def test_object_name_str(self):
        client = Client.objects.get(id=1)
        expected_object_name = f'{client.username}: {client.name} {client.surname}'
        self.assertEquals(expected_object_name, str(client))
    
 
 
class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test category')
 
    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name')
 
    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))
 
    def test_object_label_plural(self):
        category = Category.objects.get(id=1)
        object_label_plural = category._meta.verbose_name_plural
        self.assertEquals(object_label_plural, 'categories')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)



class AttractionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Localization.objects.create(street='Jana Kilińskiego 1',zipCode='15-089',city='Białystok')
        localization = Localization.objects.get(id=1)
        Category.objects.create(name='Test category')
        category = Category.objects.get(id=1)
        attraction = Attraction.objects.create(name='Test attraction',description='yes',localization=localization,timeNeededToSightsee=1.25,ticketCost=0)
        attraction.categories.set((category,))
        attraction.save()

    def test_name_label(self):
        attraction = Attraction.objects.get(id=1)
        field_label = attraction._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name') 

    def test_name_max_length(self):
        attraction = Attraction.objects.get(id=1)
        max_length = attraction._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_description_max_length(self):
        attraction = Attraction.objects.get(id=1)
        max_length = attraction._meta.get_field('description').max_length
        self.assertEquals(max_length, 500)

    def test_name_label(self):
        attraction = Attraction.objects.get(id=1)
        field_label = attraction._meta.get_field('localization').verbose_name
        self.assertEquals(field_label, 'Address')

    def test_object_name_str(self):
        attraction = Attraction.objects.get(id=1)
        expected_object_name = f'{attraction.name}'
        self.assertEquals(expected_object_name, str(attraction))

    def test_display_category(self):
        attraction = Attraction.objects.get(id=1)
        expected_return = ', '.join(category.name for category in attraction.categories.all())
        self.assertEquals(expected_return, attraction.display_category())

    def test_getTimeAsFormattedString(self):
        attraction = Attraction.objects.get(id=1)
        expected_return = '1 godzin(-a/y) 15 minut(-a)'
        self.assertEquals(expected_return, attraction.getTimeAsFormattedString())

    def test_getFormattedCost(self):
        attraction = Attraction.objects.get(id=1)
        expected_return = 'Darmowe'
        self.assertEquals(expected_return, attraction.getFormattedCost())
        


class LocalizationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Localization.objects.create(street='street',zipCode='01234',city='city')

    def test_street_label(self):
        localization = Localization.objects.get(id=1)
        field_label = localization._meta.get_field('street').verbose_name
        self.assertEquals(field_label, 'Street')

    def test_street_max_length(self):
        localization = Localization.objects.get(id=1)
        max_length = localization._meta.get_field('street').max_length
        self.assertEquals(max_length, 100)

    def test_zipcode_label(self):
        localization = Localization.objects.get(id=1)
        field_label = localization._meta.get_field('zipCode').verbose_name
        self.assertEquals(field_label, 'Zip code')

    def test_zipcode_max_length(self):
        localization = Localization.objects.get(id=1)
        max_length = localization._meta.get_field('zipCode').max_length
        self.assertEquals(max_length, 100)

    def test_city_label(self):
        localization = Localization.objects.get(id=1)
        field_label = localization._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'City')

    def test_city_max_length(self):
        localization = Localization.objects.get(id=1)
        max_length = localization._meta.get_field('city').max_length
        self.assertEquals(max_length, 100)
    
    def test_lattitude_label(self):
        localization = Localization.objects.get(id=1)
        field_label = localization._meta.get_field('lattitude').verbose_name
        self.assertEquals(field_label, 'Lattitude')

    def test_longitude_label(self):
        localization = Localization.objects.get(id=1)
        field_label = localization._meta.get_field('longitude').verbose_name
        self.assertEquals(field_label, 'Longitude')

    def test_object_name_str(self):
        localization = Localization.objects.get(id=1)
        expected_object_name = f'{localization.street}, {localization.zipCode}, {localization.city}'
        self.assertEquals(expected_object_name, str(localization))



class ShoppingCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(name='Test client',surname='Testowy')
        client = Client.objects.get(id=1)
        Localization.objects.create(street='Jana Kilińskiego 1',zipCode='15-089',city='Białystok')
        localization = Localization.objects.get(id=1)
        Category.objects.create(name='Test category')
        category = Category.objects.get(id=1)
        attraction = Attraction.objects.create(name='Test attraction',description='yes',localization=localization,timeNeededToSightsee=1.25,ticketCost=10)
        attraction.categories.set((category,))
        attraction.save()
        cart = ShoppingCart.objects.create(owner=client)
        cart.attractions.set((attraction,))
        cart.save()

    def test_owner_label(self):
        cart = ShoppingCart.objects.get(id=1)
        field_label = cart._meta.get_field('owner').verbose_name
        self.assertEquals(field_label, 'właściciel')

    def test_attractions_label(self):
        cart = ShoppingCart.objects.get(id=1)
        field_label = cart._meta.get_field('attractions').verbose_name
        self.assertEquals(field_label, 'Attraction list')

    def test_owner_username(self):
        cart = ShoppingCart.objects.get(id=1)
        client = Client.objects.get(id=1)
        username = f'{client.username}'
        self.assertEquals(username, cart.owner_username())

    def test_owner_name(self):
        cart = ShoppingCart.objects.get(id=1)
        client = Client.objects.get(id=1)
        name = f'{client.name}'
        self.assertEquals(name, cart.owner_name())

    def test_owner_surname(self):
        cart = ShoppingCart.objects.get(id=1)
        client = Client.objects.get(id=1)
        surname = f'{client.surname}'
        self.assertEquals(surname, cart.owner_surname())

    """def test_getNumberOfAttractions(self):
        cart = ShoppingCart.objects.get(id=1)
        expected_result = 1
        self.assertEquals(expected_result, cart.getNumberOfAttractions())

    def test_getTotalTime(self):
        cart = ShoppingCart.objects.get(id=1)
        expected_result = 1.25
        self.assertEquals(expected_result, cart.getTotalTime())

    def test_getTimeAsFormattedString(self):
        cart = ShoppingCart.objects.get(id=1)
        expected_result = '1 godzin(-a/y) 15 minut(-a)'
        self.assertEquals(expected_result, cart.getTimeAsFormattedString())

    def test_getTotalCost(self):
        cart = ShoppingCart.objects.get(id=1)
        expected_result = 10
        self.assertEquals(expected_result, cart.getTotalCost())
    
    def test_getFormattedCost(self):
        cart = ShoppingCart.objects.get(id=1)
        expected_result = '10.0 zł'
        self.assertEquals(expected_result, cart.getFormattedCost())"""



class TripPlanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(name='Test client',surname='Testowy')
        client = Client.objects.get(id=1)
        Localization.objects.create(street='Jana Kilińskiego 1',zipCode='15-089',city='Białystok')
        localization = Localization.objects.get(id=1)
        Category.objects.create(name='Test category')
        category = Category.objects.get(id=1)
        attraction = Attraction.objects.create(name='Test attraction',description='yes',localization=localization,timeNeededToSightsee=1.25,ticketCost=10)
        attraction.categories.set((category,))
        attraction.save()
        plan = TripPlan.objects.create(name='test_name',creator=client)
        plan.attractions.set((attraction,))
        plan.save()

    def test_name_label(self):
        plan = TripPlan.objects.get(id=1)
        field_label = plan._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name')

    def test_creator_label(self):
        plan = TripPlan.objects.get(id=1)
        field_label = plan._meta.get_field('creator').verbose_name
        self.assertEquals(field_label, 'Creator')
        
    def test_attraction_label(self):
        plan = TripPlan.objects.get(id=1)
        field_label = plan._meta.get_field('attractions').verbose_name
        self.assertEquals(field_label, 'Attraction list')

    def test_object_name_str(self):
        plan = TripPlan.objects.get(id=1)
        expected_object_name = f'{plan.name}'
        self.assertEquals(expected_object_name, str(plan))

    def test_getNumberOfAttractions(self):
        plan = TripPlan.objects.get(id=1)
        expected_result = 1
        self.assertEquals(expected_result, plan.getNumberOfAttractions())

    def test_getTotalTime(self):
        plan = TripPlan.objects.get(id=1)
        expected_result = 1.25
        self.assertEquals(expected_result, plan.getTotalTime())

    def test_getFormattedTime(self):
        plan = TripPlan.objects.get(id=1)
        expected_result = '1 godzin(-a/y) 15 minut(-a)'
        self.assertEquals(expected_result, plan.getFormattedTime())

    def test_getTotalCost(self):
        plan = TripPlan.objects.get(id=1)
        expected_result = 10
        self.assertEquals(expected_result, plan.getTotalCost())
    
    def test_getFormattedCost(self):
        plan = TripPlan.objects.get(id=1)
        expected_result = '10.0 zł'
        self.assertEquals(expected_result, plan.getFormattedCost())