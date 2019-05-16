from django.db.models.signals import post_save
from django.dispatch import receiver
from . import google_maps_api

from guide.models import Client, ShoppingCart, Localization, Attraction


@receiver(post_save, sender=Client)
def createShoppingCartForClient(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(owner=instance)


@receiver(post_save, sender=Attraction)
def populateAttractionsGeoCoordinates(sender, instance, created, **kwargs):
    if created:
        apiResponse = google_maps_api.search_place(
            ''+instance.name+' '+instance.localization.street+''+instance.localization.zipCode+' '+instance.localization.city)
        instance.localization.lattitude = apiResponse['geometry']['location']['lat']
        instance.localization.longitude = apiResponse['geometry']['location']['lng']
        instance.localization.save()
