"""Campingbenin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from Campingbenin.camping.views import event_list_view
from camping import views
from django.contrib import admin
from django.urls import path
from camping.views import event_list_view, create_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('erreur/', views.erreur_paiement, name='erreur'),
    path('reservation/', views.reservation, name='reservation'),
    path('event_create/', views.event_create, name='event_create'),
    path('carou/', views.carou, name='carou'),
    path('view/', views.view, name='view'),
    path('event_details/', views.event_details, name='event_details'),
    path('', event_list_view, name='event_list'),
    path('get_event/', views.get_event, name='get_event'),
    path('api/create-reservation/', create_reservation, name='create_reservation'),
    # path('confirmation/', views.confirmation_reservation, name='confirmation_reservation'),
    path('confirmation/<int:reservation_id>/', views.confirmation_reservation, name='confirmation_reservation'),
    # URL pour gérer le retour de paiement
    path('paiement_retour/', views.paiement_retour, name='paiement_retour'),

]
