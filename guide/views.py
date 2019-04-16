from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart
# Create your views here.


def home(request):
    return render(request, 'home.html')


class AttractionListView(ListView):
    model = Attraction


class AttractionDetailView(DetailView):
    model = Attraction


class TripPlanListView(ListView):
    model = TripPlan


class TripPlanDetailView(DetailView):
    model = TripPlan


class ShoppingCartDetailView(DetailView):
    model = ShoppingCart
