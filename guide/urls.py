from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attractions', views.AttractionListView.as_view(), name='attractions'),
    path('attractions/<int:pk>',
         views.AttractionDetailView.as_view(), name='attraction-detail'),
    path('shoppingcart',
         views.shoppingCartView, name='shopping-cart'),
    path('addattraction/<int:pk>',
         views.addAttraction, name='add-attraction'),
    path('removeattraction/<int:pk>',
         views.removeAttraction, name='remove-attraction'),
    path('tripplans', views.TripPlanListView.as_view(), name='tripplans'),
    path('tripplans/<int:pk>', views.TripPlanDetailView.as_view(),
         name='tripplans-detail'),
    path("mytripplans", views.MyTripPlanListView.as_view(), name="mytripplans"),
    path("mytripplans/<int:pk>", views.MyTripPlanDetailView.as_view(),
         name="mytripplans-detail"),

]
