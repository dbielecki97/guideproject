from django.db.models.signals import post_save
from django.dispatch import receiver
from . import google_maps_api

from guide.models import Client, ShoppingCart, Localization, Attraction


@receiver(post_save, sender=Client)
def createShoppingCartForClient(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(owner=instance)


@receiver(post_save, sender=Attraction)
def createAddPopulateLocalization(sender, instance, created, **kwargs):
    if created:
        loc = Localization.objects.create(formattedAddress=google_maps_api.search_place(
            instance.name)['formatted_address'])
        instance.localization = loc
        instance.save()
