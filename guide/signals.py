from django.db.models.signals import post_save
from django.dispatch import receiver

from guide.models import Client, ShoppingCart


@receiver(post_save, sender=Client)
def createShoppingCartForClient(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(owner=instance)
