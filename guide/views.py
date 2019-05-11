from . import google_maps_api
import simplejson
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart
from .forms import SaveTripPlanForm, SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.views.generic import FormView
from django.contrib.auth import authenticate, login


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
        if self.request.user.pk:
            user = Client.objects.get(pk=self.request.user.pk)
            attractionNamesInCreator = ShoppingCart.objects.get(
                owner=user).attractions.values_list('name', flat=True).all()
            context["attractionNamesInCreator"] = attractionNamesInCreator
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locationsInfo = getAttractionsInfo(self.object.attractions.all())
        context["locationsInfo"] = locationsInfo
        context["numberOfLocations"] = len(locationsInfo)
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
        attractionsInfo = getAttractionsInfo(attractions)
        context["locationsInfo"] = simplejson.dumps(
            attractionsInfo)
        context['numberOfLocations'] = len(attractionsInfo)
        print(len(attractionsInfo))
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


class SignUp(FormView):
    form_class = SignUpForm
    success_url = 'home'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


def removeMyPlan(request, pk):
    tripPlan = get_object_or_404(TripPlan, pk=pk).delete()
    return HttpResponseRedirect(reverse('my-trip-plans'))

def accountManagement(request):
    return render(request, 'account/myaccount.html')
        

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/changepassword.html', {
        'form': form
    })
