from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('attractions', views.AttractionListView.as_view(), name='attractions'),
    path('attractions/<int:pk>',
         views.AttractionDetailView.as_view(), name='attraction-detail'),
    path('shoppingcart',
         views.ShoppingCartView.as_view(), name='shopping-cart'),
    path('addattraction/<int:pk>',
         views.addAttraction, name='add-attraction'),
    path('removeattractionfromplan/<int:trip_pk>/<int:attr_pk>',
         views.removeAttractionFromPlan, name='remove-attraction-from-plan'),
    path('removeattractionfromshoppingcart/<int:pk>',
         views.removeAttractionFromShoppingCart, name='remove-attraction-from-shopping-cart'),
    path('saveplan/<int:pk>',
         views.saveTripPlan, name='save-trip-plan'),
    path('tripplans', views.TripPlanListView.as_view(), name='trip-plans'),
    path('tripplan/<int:pk>', views.TripPlanDetailView.as_view(),
         name='trip-plan-detail'),
    path("mytripplans", views.MyTripPlanListView.as_view(), name="my-trip-plans"),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('removemyplan/<int:pk>', views.removeMyPlan, name='remove-my-plan'),
    path('editmyplan/<int:pk>', views.EditPlanView.as_view(), name='edit-my-plan'),
    path('changename/<int:pk>', views.changeNameOfPlan, name='change-name'),
    path('myaccount/general', views.generalSettings, name='general'),
    path('myaccount/changepassword', views.change_password, name='change-password')
]
