from django.contrib import admin
from guide.models import Attraction, Category, Client, Localization, ShoppingCart, TripPlan

# Register your models here.
admin.site.register(Attraction)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Localization)
admin.site.register(ShoppingCart)
admin.site.register(TripPlan)
