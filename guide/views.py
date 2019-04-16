from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Attraction, TripPlan, Localization, Category, Client, ShoppingCart
from django.utils import timezone
import simplejson
# Create your views here.


def home(request):
    return render(request, 'home.html')


class AttractionListView(ListView):
    model = Attraction

    def getPositions(self):
        pos = []
        for obj in self.object_list:
            pos.append({"lat": obj.localization.latitude,
                        "lgt": obj.localization.longitude})
        return pos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["localizations"] = simplejson.dumps(self.getPositions())
        return context


class AttractionDetailView(DetailView):
    model = Attraction

    def getLongTimeNeededToSoghtsee(self):
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
        context['longTimeNeededToSightsee'] = self.getLongTimeNeededToSoghtsee()
        return context


class TripPlanListView(ListView):
    model = TripPlan


class TripPlanDetailView(DetailView):
    model = TripPlan


class ShoppingCartDetailView(DetailView):
    model = ShoppingCart
