from . import google_maps_api
import simplejson
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart


def home(request):
    return render(request, 'home.html')


class AttractionListView(ListView):
    model = Attraction

    def getAttractionsInfo(self):
        pos = []
        for obj in self.object_list:
            pos.append({"name": obj.name, "lat": obj.localization.latitude,
                        "lng": obj.localization.longitude})
        return pos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locationsInfo"] = simplejson.dumps(self.getAttractionsInfo())
        return context


class AttractionDetailView(DetailView):
    model = Attraction

    def getAttractionsInfo(self):
        pos = {"name": self.object.name, "lat": self.object.localization.latitude,
               "lng": self.object.localization.longitude}
        return pos

    def getLongTimeNeededToSightsee(self):
        hours = int(self.object.timeNeededToSightsee)
        minutes = int((self.object.timeNeededToSightsee % 1)*60)
        result = ''
        if hours:
            if hours == 1:
                result += str(hours) + ' godzina'
            else:
                result += str(hours) + ' godzin'
        if minutes:
            result += ' '+str(minutes) + ' minut'
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['longTimeNeededToSightsee'] = self.getLongTimeNeededToSightsee()
        context['locationInfo'] = self.getAttractionsInfo()
        return context


class TripPlanListView(ListView):
    model = TripPlan

    def get_queryset(self):
        return TripPlan.objects.filter(creator__isnull=True)


class TripPlanDetailView(DetailView):
    model = TripPlan

    def getAttractionsInfo(self):
        pos = []
        for obj in self.object.attractions.all():
            pos.append({"name": obj.name, "lat": obj.localization.latitude,
                        "lng": obj.localization.longitude})
        return pos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locationsInfo"] = self.getAttractionsInfo()
        return context


class MyTripPlanListView(ListView):
    model = TripPlan
    template_name = "guide/mytripplan_list.html"
    context_object_name = "mytripplans"

    def get_queryset(self):
        return TripPlan.objects.filter(creator=self.request.user)


class MyTripPlanDetailView(DetailView):
    model = TripPlan
    template_name = "mytripplan_detail.html"


def shoppingCartView(request):
    shoppingCart = ShoppingCart.objects.get(owner=request.user)
    attractions = shoppingCart.attractions.all
    context = {
        'attractions': attractions,
    }
    return render(request, 'guide/shoppingcart.html', context)


def addAttraction(request, pk):
    attractionInstance = get_object_or_404(Attraction, pk=pk)
    clientInstance = get_object_or_404(Client, pk=request.user.pk)
    shoppingCartInstance = get_object_or_404(
        ShoppingCart, owner=clientInstance)
    shoppingCartInstance.attractions.add(attractionInstance)
    return HttpResponseRedirect(reverse('attractions'))


def removeAttraction(request, pk):
    attractionInstance = get_object_or_404(Attraction, pk=pk)
    clientInstance = get_object_or_404(Client, pk=request.user.pk)
    shoppingCartInstance = get_object_or_404(
        ShoppingCart, owner=clientInstance)
    shoppingCartInstance.attractions.remove(attractionInstance)
    return HttpResponseRedirect(reverse('shopping-cart'))
