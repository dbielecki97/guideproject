from . import google_maps_api
import simplejson
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart
from .forms import SaveTripPlanForm


def home(request):
    return render(request, 'home.html')


def getAttractionsInfo(attractions):
    pos = []
    for attraction in attractions:
        pos.append({"name": attraction.name, "lat": attraction.localization.latitude,
                    "lng": attraction.localization.longitude})
    return pos


class AttractionListView(ListView):
    model = Attraction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locationsInfo"] = simplejson.dumps(
            getAttractionsInfo(self.object_list))
        return context


def getTimeAsFormattedString(time):
    hours = int(time)
    minutes = int((time % 1)*60)
    result = ''
    if hours:
        result += str(hours) + ' godzin(-a/y) '
    if minutes:
        result += str(minutes) + ' minut(-a)'
    return result


def getFormattedCost(ammount):
    formattedAmmound = ''
    if ammount == 0:
        formattedAmmound = 'Darmowe'
    else:
        formattedAmmound += str(ammount) + ' zł'
    return formattedAmmound


class AttractionDetailView(DetailView):
    model = Attraction

    def getAttractionInfo(self):
        pos = {"name": self.object.name, "lat": self.object.localization.latitude,
               "lng": self.object.localization.longitude}
        return pos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timeasformattedstring'] = getTimeAsFormattedString(
            self.object.timeNeededToSightsee)
        context['locationInfo'] = self.getAttractionInfo()
        context['ticketCost'] = getFormattedCost(self.object.ticketCost)
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


class ShoppingCartView(TemplateView):
    template_name = 'guide/shoppingcart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoppingCart = ShoppingCart.objects.get(owner=self.request.user)
        attractions = shoppingCart.attractions.all()
        totalTime = 0
        totalCost = 0
        for attraction in attractions:
            totalTime += attraction.timeNeededToSightsee
        for attraction in attractions:
            totalCost += attraction.ticketCost
        context['shoppingcart'] = shoppingCart
        context['attractions'] = attractions
        context['totalTime'] = getTimeAsFormattedString(totalTime)
        context['totalCost'] = getFormattedCost(totalCost)
        context['form'] = SaveTripPlanForm
        context["locationsInfo"] = simplejson.dumps(
            getAttractionsInfo(attractions))
        return context


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


def saveTripPlan(request, pk):
    if request.method == 'POST':
        form = SaveTripPlanForm(request.POST)
        if form.is_valid():
            tripplan = TripPlan.objects.create(creator=Client.objects.get(
                pk=request.user.pk), name=form.cleaned_data['name'])
            tripplan.attractions.set(ShoppingCart.objects.get(
                pk=pk).attractions.all())
            tripplan.save()

    return HttpResponseRedirect(reverse('my-trip-plans'))
