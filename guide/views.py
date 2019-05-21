from django.contrib.auth.decorators import login_required
from . import google_maps_api
import imghdr
import simplejson
import types
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart
from .forms import SaveTripPlanForm, SignUpForm, CustomUserChangeForm, ChangeTripPlanNameForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.views.generic import FormView
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import UserChangeForm
import sys

from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'home.html')


def extractInfo(attractionList):
    formattedInfo = []
    try:
        for attraction in attractionList:
            formattedInfo.append({'name': attraction.name,
                                  'lat-lng': {'lat': attraction.localization.lattitude, 'lng': attraction.localization.longitude}})
        return formattedInfo
    except:
        pass
    try:
        formattedInfo.append({'name': attractionList.name,
                              'lat-lng': {'lat': attractionList.localization.lattitude, 'lng': attractionList.localization.longitude}})
        return formattedInfo
    except:
        pass


class AttractionListView(ListView):
    model = Attraction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            attractions = ShoppingCart.objects.get(
                owner=self.request.user).attractions.all()
            attractionPKs = attractions.values_list('pk')
            availableAttractions = Attraction.objects.exclude(
                pk__in=attractionPKs)
            context['availableAttractions'] = availableAttractions
        return context


class AttractionDetailView(DetailView):
    model = Attraction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attractionLocalization'] = extractInfo(self.object)
        try:
            shoppingcart = ShoppingCart.objects.get(owner=self.request.user)
            if shoppingcart.attractions.filter(pk=self.object.pk):
                context['inPlan'] = True
        except:
            pass
        return context


class TripPlanListView(ListView):
    model = TripPlan

    def get_queryset(self):
        return TripPlan.objects.filter(creator__isnull=True)


class TripPlanDetailView(DetailView):
    model = TripPlan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attractionLocalizations = extractInfo(self.object.attractions.all())
        context["attractionLocalizations"] = attractionLocalizations
        hours, minutes = self.object.getTotalTimeSplit()
        context['hours'] = hours
        context['minutes'] = minutes
        if self.request.user.is_authenticated and self.request.user.pk == self.object.creator.pk:
            attractions = ShoppingCart.objects.get(
                owner=self.request.user).attractions.all()
            availableAttractions = Attraction.objects.exclude(
                pk__in=attractions.values_list('pk'))
            context['availableAttractions'] = availableAttractions
            context['changeNameForm'] = ChangeTripPlanNameForm
        return context


class MyTripPlanListView(LoginRequiredMixin, ListView):
    model = TripPlan
    template_name = "guide/mytripplan_list.html"
    context_object_name = "mytripplans"

    def get_queryset(self):
        return TripPlan.objects.filter(creator=self.request.user)


class ShoppingCartView(LoginRequiredMixin, TemplateView):
    template_name = 'guide/shoppingcart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoppingCart = ShoppingCart.objects.get(owner=self.request.user)
        attractions = shoppingCart.attractions.all()
        attractionPKs = attractions.values_list('pk')
        availableAttractions = Attraction.objects.exclude(pk__in=attractionPKs)
        context['shoppingcart'] = shoppingCart
        context['attractions'] = attractions
        context['saveform'] = SaveTripPlanForm
        context['availableattractions'] = availableAttractions
        attractionLocalizations = extractInfo(attractions)
        context["attractionLocalizations"] = attractionLocalizations
        return context


@login_required
def addAttractionToShoppingCart(request, pk):
    attractionInstance = get_object_or_404(Attraction, pk=pk)
    clientInstance = get_object_or_404(Client, pk=request.user.pk)
    shoppingCartInstance = get_object_or_404(
        ShoppingCart, owner=clientInstance)
    shoppingCartInstance.attractions.add(attractionInstance)
    return HttpResponseRedirect(reverse('attractions'))


@login_required
def addAttractionToTripPlan(request, trip_pk, attraction_pk):
    attractionInstance = get_object_or_404(Attraction, pk=attraction_pk)
    clientInstance = get_object_or_404(Client, pk=request.user.pk)
    tripPlanInstance = get_object_or_404(
        TripPlan, pk=trip_pk)
    tripPlanInstance.attractions.add(attractionInstance)
    return HttpResponseRedirect(reverse('trip-plan-detail', kwargs={'pk': trip_pk}))


@login_required
def removeAttractionFromShoppingCart(request, pk):
    attractionInstance = get_object_or_404(Attraction, pk=pk)
    clientInstance = get_object_or_404(Client, pk=request.user.pk)
    shoppingCartInstance = get_object_or_404(
        ShoppingCart, owner=clientInstance)
    shoppingCartInstance.attractions.remove(attractionInstance)
    return HttpResponseRedirect(reverse('shopping-cart'))


@login_required
def removeAttractionFromPlan(request, trip_pk, attr_pk):
    attractionInstance = get_object_or_404(Attraction, pk=attr_pk)
    tripplan = get_object_or_404(TripPlan, pk=trip_pk)
    tripplan.attractions.remove(attractionInstance)
    return HttpResponseRedirect(reverse('trip-plan-detail', kwargs={'pk': trip_pk}))


@login_required
def saveTripPlan(request, pk):
    if request.method == 'POST':
        form = SaveTripPlanForm(request.POST)
        if form.is_valid():
            tripplan = TripPlan.objects.create(creator=Client.objects.get(
                pk=request.user.pk), name=form.cleaned_data['name'])
            shoppingcart = ShoppingCart.objects.get(pk=pk)
            tripplan.attractions.set(shoppingcart.attractions.all())
            shoppingcart.attractions.clear()
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


@login_required
def removeMyPlan(request, pk):
    tripPlan = get_object_or_404(TripPlan, pk=pk).delete()
    return HttpResponseRedirect(reverse('my-trip-plans'))


@login_required
def changeNameOfPlan(request, pk):
    if request.method == 'POST':
        form = ChangeTripPlanNameForm(request.POST)
        if form.is_valid():
            tripplan = TripPlan.objects.get(pk=pk)
            tripplan.name = form.cleaned_data['name']
            tripplan.save()

    return HttpResponseRedirect(reverse('trip-plan-detail', kwargs={'pk': pk}))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'account/changepassword.html', {
        'form': form
    })


@login_required
def generalSettings(request):
    client = get_object_or_404(Client, pk=request.user.pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, instance=request.user, initial=None)
        if form.is_valid():
            cd = form.cleaned_data
            client.email = cd['email'] or ''
            client.name = cd['name'] or ''
            client.surname = cd['surname'] or ''
            client.save()
            messages.success(
                request, 'Your settings were successfully updated!')
            return redirect('general')
    else:
        form = CustomUserChangeForm(instance=request.user, initial={
            'name': client.name,
            'surname': client.surname
        })
    return render(request, "account/general.html", {
        'form': form
    })
