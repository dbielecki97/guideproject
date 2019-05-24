from django.contrib import admin
from guide.models import Attraction, Category, Client, Localization, ShoppingCart, TripPlan


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'localization', 'display_category',
                    'timeNeededToSightsee', 'ticketCost')
    list_filter = ('timeNeededToSightsee', 'ticketCost', 'categories')

    fieldsets = (
        ('General', {
            'fields': ('name', 'description', 'categories', 'timeNeededToSightsee', 'ticketCost')
        }),
        ('Localization', {
            'fields': ('localization',)
        })
    )


admin.site.register(Category)
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname')
    fieldsets = (
        ('Login information', {
            'fields': ('username', 'password', 'last_login', 'date_joined'),
        }),
        ('General', {
            'fields': ('name', 'surname', 'email')
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'password')


@admin.register(Localization)
class LocalizationAdmin(admin.ModelAdmin):
    list_display = ('street', 'zipCode', 'city')
    fieldsets = (
        ('Address information', {
            'fields': ('street', 'zipCode', 'city'),
        }),
        ('Geopraphical coordinates', {
            'fields': ('lattitude', 'longitude')
        }),
    )
    readonly_fields = ('lattitude', 'longitude')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner_name', 'owner_surname', 'owner_username')


@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator',)
