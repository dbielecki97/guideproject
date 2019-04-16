from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attractions', views.AttractionListView.as_view(), name='attractions'),
    path('attractions/<int:pk>',
         views.AttractionDetailView.as_view(), name='attraction-detail'),
    path('shoppingcard/<int:pk>',
         views.ShoppingCartDetailView.as_view(), name='shopping-cart'),
    path('mytripplans/', views.TripPlanListView.as_view(), name='my-trip-plans'),
    path('mytripplans/<int:pk>', views.TripPlanDetailView.as_view(),
         name='trip-plan-detail'),
]
