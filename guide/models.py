from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Client(User):
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True)
    surname = models.CharField(
        _("Surname"), max_length=50, null=True, blank=True)

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
        "Localization", verbose_name=_("Address"), on_delete=models.SET_NULL, null=True)
    timeNeededToSightsee = models.FloatField(
        _("Time neede to sightsee (in hours)"))
    ticketCost = models.FloatField(
        _("Ticket's cost"), default=0)

    def __str__(self):
        return self.name


class Localization(models.Model):
    street = models.CharField(
        _("Street"), max_length=100, help_text='Name of the street')
    zipCode = models.CharField(
        _("Zipcode"), max_length=10, help_text='Zip code')
    city = models.CharField(_("City"), max_length=50)
    latitude = models.FloatField(_("Latitude"), null=True)
    longitude = models.FloatField(_("Longitude"), null=True)
    voivodeship = models.CharField(_("Voivodeship"), max_length=50)

    def __str__(self):
        return '' + self.street + ' '+self.zipCode+', ' + self.city+', '+self.voivodeship


class ShoppingCart(models.Model):
    owner = models.ForeignKey("Client", verbose_name=_(
        "Owner"), on_delete=models.CASCADE)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"))


class TripPlan(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    creator = models.ForeignKey("Client", verbose_name=_(
        "Creator"), on_delete=models.CASCADE, null=True, blank=True)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"))

    def __str__(self):
        return ''+self.name
