from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Client(User):
    name = models.CharField(_("Name"), max_length=50,
                            null=True, blank=True, default="")
    surname = models.CharField(
        _("Surname"), max_length=50, null=True, blank=True, default="")

    def __str__(self):
        return ''+self.name+' '+self.surname

    class Meta:
        verbose_name = "client"


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Attraction(models.Model):
    name = models.CharField(_("Name"),
                            max_length=200, help_text="Enter attraction's name.")
    description = models.TextField(max_length=500)
    categories = models.ManyToManyField(
        "Category")
    localization = models.ForeignKey(
        "Localization", verbose_name=_("Address"), on_delete=models.CASCADE, null=True, blank=True)
    timeNeededToSightsee = models.FloatField(
        _("Time neede to sightsee (in hours)"))
    ticketCost = models.FloatField(
        _("Ticket's cost"), default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Localization(models.Model):
    formattedAddress = models.CharField(_("Address"), max_length=150)

    def __str__(self):
        return self.formattedAddress


class ShoppingCart(models.Model):
    owner = models.ForeignKey("Client", verbose_name=_(
        "właściciel"), on_delete=models.CASCADE)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"), blank=True)


class TripPlan(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    creator = models.ForeignKey("Client", verbose_name=_(
        "Creator"), on_delete=models.CASCADE, null=True, blank=True)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"))

    def __str__(self):
        return '' + self.name

    class Meta:
        ordering = ['name']
