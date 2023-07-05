from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import EventForm, ReservationForm
from django.contrib import messages
from .models import Event, ImageObjet,Reservation, ReservationConfirmation
from django.utils import timezone
from datetime import datetime
import kkiapay


# from kkiapay import KkiapayWidget
# from .forms import ReservationForm
# Create your views here.

def index(request):
    return render(request, 'Campingbenin/index.html')

def reservation(request):
    return render(request, 'Campingbenin/reservation.html')   

def event_create(request):
    return render(request, 'Campingbenin/event_create.html')

def event_details(request):
    return render(request, 'Campingbenin/event_details.html')

def carou(request):
    return render(request, 'Campingbenin/carou.html')

def confirmation_paiement(request):
    return render(request, 'Campingbenin/confirmation_paiement.html')

def erreur_paiement(request):
    return render(request, 'Campingbenin/erreur_paiement.html')

def view(request):
    return render(request, 'Campingbenin/view.html')

#Créez une vue pour afficher le formulaire de création d'événement :
def event_create_view(request):
    form = EventForm()
    return render(request, 'event_create.html', {'form': form})

# Créez une vue pour enregistrer l'événement créé :
def event_create_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre événement a été créé avec succès.')
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})

# def event_list_view(request):
#     events = Event.objects.all()
#     return render(request, 'Campingbenin/Index.html', {'events': events})

def event_list_view(request):
  events = Event.objects.all()

  # Créez un dictionnaire pour stocker les images pour chaque événement
  event_images = {}

  # Parcourez chaque événement
  for event in events:
      # Obtenez toutes les images associées à cet événement
     images = ImageObjet.objects.filter(object=event)
      # Stockez les images dans le dictionnaire en utilisant l'ID de l'événement comme clé
     event_images[event.id] = images

  # Renvoyer les événements et les images associées à chaque événement dans le contexte de rendu
  return render(request, 'Campingbenin/Index.html', {'events': events, 'event_images': event_images})

# def event_details(request, event_id):
#     event = Event.objects.get(id=event_id)
#     image = ImageObjet.objects.filter(object=event).first()
#     context = {
#         'event': event,
#         'image': image,
#     }
#     return render(request, 'event_list.html', context)
   # Créez une vue pour afficher les détails de l'événement :
# def event_detail_view(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)
#     return render(request, 'event_detail.html', {'event': event})

# Créez une vue pour afficher tous les événements à venir :
def events_view(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events.html', {'events': events})

# Ajoutez une vue pour confirmer la réservation :

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            confirmation_number = 'ABC123' # Remplacez par une logique pour générer un numéro de confirmation unique
            confirmation = ReservationConfirmation(reservation=reservation, confirmation_number=confirmation_number)
            confirmation.save()
            messages.success(request, 'Votre réservation a été confirmée avec succès.')
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})


def my_view(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'my_template.html', context=context)

def get_event(request):
    event_id = request.GET.get('event_id')
    event = Event.objects.get(pk=event_id)
    response_data = {
        'name': event.name,
        'description': event.description,
    }
    return JsonResponse(response_data)

def reservation_view(request):
    event = get_object_or_404(Event, pk=1)  # Récupérer l'événement concerné par la réservation
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            num_reserved = form.cleaned_data['num_of_people']
            if num_reserved <= event.num_of_seats:
                reservation = form.save()
                confirmation_number = 'ABC123'  # Remplacez par une logique pour générer un numéro de confirmation unique
                confirmation = ReservationConfirmation(reservation=reservation, confirmation_number=confirmation_number)
                confirmation.save()
                # Mettre à jour le nombre de places disponibles pour l'événement
                event.num_of_seats -= num_reserved
                event.save()
                messages.success(request, 'Votre réservation a été confirmée avec succès.')
                return redirect('home')
            else:
                messages.error(request, 'Le nombre de places restantes est insuffisant pour votre réservation.')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})
#  Ajoutez une vue pour afficher les réservations à venir :

def reservations_view(request):
    reservations = Reservation.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'reservations.html', {'reservations': reservations})

# @csrf_exempt
# def create_reservation(request):
#     if request.method == 'POST':
#         client_name = request.POST.get('name')
#         client_email = request.POST.get('mail')
#         client_phone = request.POST.get('numeroTelephone')
#         date = request.POST.get('date')
#         party_size = request.POST.get('size')
#         total_amount = request.POST.get('total')
        
#           # Obtient l'heure actuelle
#         current_time = datetime.now().time()  
       

#         reservation = Reservation(
#             client_name=client_name,
#             client_email=client_email,
#             client_phone=client_phone,
#             date=date,
#             time=current_time,
#             party_size=party_size,
#             total_amount=total_amount
#         )
#         reservation.save()
        
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})
    
#     import requests

# @csrf_exempt
# def create_reservation(request):
#     if request.method == 'POST':
#         client_name = request.POST.get('name')
#         client_email = request.POST.get('mail')
#         client_phone = request.POST.get('numeroTelephone')
#         date = request.POST.get('date')
#         party_size = request.POST.get('size')
#         total_amount = request.POST.get('total')
        
#           # Obtient l'heure actuelle
#         current_time = datetime.now().time()  
       

#         reservation = Reservation(
#             client_name=client_name,
#             client_email=client_email,
#             client_phone=client_phone,
#             date=date,
#             time=current_time,
#             party_size=party_size,
#             total_amount=total_amount
#         )
#         reservation.save()

#         return redirect(redirec)
#     else:
#         return JsonResponse({'status': 'error'})
 

# def create_reservation(request):
#   if request.method == 'POST':
#     client_name = request.POST.get('name')
#     client_email = request.POST.get('mail')
#     client_phone = request.POST.get('numeroTelephone')
#     date = request.POST.get('date')
#     party_size = request.POST.get('size')
#     total_amount = request.POST.get('total')
    
#     # Obtient l'heure actuelle
#     current_time = datetime.now().time()  

#     reservation = Reservation(
#       client_name=client_name,
#       client_email=client_email,
#       client_phone=client_phone,
#       date=date,
#       time=current_time,
#       party_size=party_size,
#       total_amount=total_amount
#     )
#     reservation.save()
#     secret_code= 'sk_206cbbe877ad89bc67e923978abafd1f27a50979a1a3d14c859d183fb9bfd3a1'
#     try:
#       api = kkiapay.Api(secret_code)
#       payment_request = api.request_payment(amount=total_amount, description='Paiement reservation', currency='XOF', metadata='', callback_url='http://127.0.0.1:9000/paiement_retour/')
          
#     except Exception as e:
#       print('Error: %s' % str(e))
      
#     if payment_request is not None:
#         return HttpResponseRedirect(payment_request.payment_url)

#   else:
#     return JsonResponse({'status': 'error'})


def create_reservation(request):
    if request.method == 'POST':
        client_name = request.POST.get('name')
        client_email = request.POST.get('mail')
        client_phone = request.POST.get('numeroTelephone')
        date = request.POST.get('date')
        party_size = request.POST.get('size')
        total_amount = request.POST.get('total')
        
        # Obtient l'heure actuelle
        current_time = datetime.now().time()  
    
        reservation = Reservation(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            date=date,
            time=current_time,
            party_size=party_size,
            total_amount=total_amount
        )
        reservation.save()
        
        # Redirige l'utilisateur vers la page de récapitulatif de réservation
        return redirect('confirmation_reservation', reservation_id=reservation.id)
        
    else:
        return JsonResponse({'status': 'error'})

def confirmation_reservation(request, reservation_id):
    
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'Campingbenin/confirmation_reservation.html', {'reservation': reservation})
    #reservation = Reservation.objects.last()
      # Afficher la page de confirmation avec les détails de la réservation et le bouton de paiement
    #return render(request, 'Campingbenin/confirmation_reservation.html', {'reservation': reservation})
    
    
    
    
def paiement_retour(request):
    payment_id = request.GET.get('payment_id')
    transaction_id = request.GET.get('transaction_id')
    status = request.GET.get('status')
    
    if payment_id is None or transaction_id is None or status is None:
        return HttpResponseBadRequest('Requête invalide')

    if status == 'PAID':
        # Mettre à jour l'état de la réservation en fonction de l'ID de paiement
        reservation = Reservation.objects.get(payment_id=payment_id)
        reservation.status = 'PAID'
        reservation.save()
        # Rediriger l'utilisateur vers une page de confirmation de paiement réussi
        return redirect('confirmation_paiement')
    else:
        # Rediriger l'utilisateur vers une page d'erreur de paiement
        return redirect('erreur_paiement')
