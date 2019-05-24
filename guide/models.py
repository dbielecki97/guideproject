import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Client(User):
    name = models.CharField(_("Name"), max_length=50,
                            null=True, blank=True, default="")
    surname = models.CharField(
        _("Surname"), max_length=50, null=True, blank=True, default="")

    def __str__(self):
        return ''+self.username+': '+self.name+' '+self.surname

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

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.categories.all())

    def getTimeAsFormattedString(self):
        hours = int(self.timeNeededToSightsee)
        minutes = int((self.timeNeededToSightsee % 1)*60)
        result = ''
        if hours:
            result += str(hours) + ' godzin(-a/y) '
        if minutes:
            result += str(minutes) + ' minut(-a)'
        return result

    def getFormattedCost(self):
        if self.ticketCost == 0:
            return 'Darmowe'
        else:
            return f'{str(self.ticketCost)} zł'

    display_category.short_description = 'Category'

    class Meta:
        ordering = ['name']


class Localization(models.Model):
    street = models.CharField(_("Street"), max_length=100)
    zipCode = models.CharField(_("Zip code"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    lattitude = models.FloatField(_("Lattitude"), default=0)
    longitude = models.FloatField(_("Longitude"), default=0)

    def __str__(self):
        return self.street+', '+self.zipCode+', '+self.city


class ShoppingCart(models.Model):
    owner = models.ForeignKey("Client", verbose_name=_(
        "właściciel"), on_delete=models.CASCADE)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"), blank=True)

    def owner_username(self):
        return self.owner.username

    def owner_name(self):
        return self.owner.name

    def owner_surname(self):
        return self.owner.surname

    def getNumberOfAttractions(self):
        return len(attractions)

    def getTotalCost(self):
        tCost = 0
        for attraction in self.attractions.all():
            tCost += attraction.ticketCost
        return tCost

    def getTotalTime(self):
        tTime = 0
        for attraction in self.attractions.all():
            tTime += attraction.timeNeededToSightsee
        return tTime

    def getTimeAsFormattedString(self):
        time = self.getTotalTime()
        hours = int(time)
        minutes = int((time % 1)*60)
        result = ''
        if hours:
            result += str(hours) + ' godzin(-a/y) '
        if minutes:
            result += str(minutes) + ' minut(-a)'
        return result

    def getFormattedCost(self):
        totalTime = self.getTotalCost()
        if totalTime == 0:
            return 'Darmowe'
        else:
            return f'{totalTime} zł'


class TripPlan(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    creator = models.ForeignKey("Client", verbose_name=_(
        "Creator"), on_delete=models.CASCADE, null=True, blank=True)
    attractions = models.ManyToManyField(
        "Attraction", verbose_name=_("Attraction list"))

    def __str__(self):
        return '' + self.name

    def getNumberOfAttractions(self):
        return len(self.attractions.all())

    def getTotalTime(self):
        totalTime = 0
        for attraction in self.attractions.all():
            totalTime += attraction.timeNeededToSightsee
        return totalTime

    def getTotalTimeSplit(self):
        totalTime = self.getTotalTime()
        return math.floor(totalTime), round((totalTime-math.floor(totalTime))*60)

    def getFormattedTime(self):
        time = self.getTotalTime()
        hours = int(time)
        minutes = int((time % 1)*60)
        result = ''
        if hours:
            result += str(hours) + ' godzin(-a/y) '
        if minutes:
            result += str(minutes) + ' minut(-a)'
        return result

    def getTotalCost(self):
        totalPrice = 0
        for attraction in self.attractions.all():
            totalPrice += attraction.ticketCost
        return totalPrice

    def getFormattedCost(self):
        totalTime = self.getTotalCost()
        if totalTime == 0:
            return 'Darmowe'
        else:
            return f'{totalTime} zł'

    class Meta:
        ordering = ['name']
