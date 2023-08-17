from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import EventForm, ReservationForm
from django.contrib import messages
from .models import Event, ImageObjet,Reservation, ReservationConfirmation
from django.utils import timezone
from datetime import datetime
from kkiapay import Kkiapay
from .models import Testimonial
import qrcode
from django.core.paginator import Paginator
from django.views.generic import View
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import base64

def index(request):
    return render(request, 'Campingbenin/index.html')

def reservation_pass(request):
    return render(request, 'Campingbenin/reservation_pass.html')

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

def erreur_paiement(request):
    return render(request, 'Campingbenin/erreur_paiement.html')

def confirmation_paiement(request):
    return render(request, 'Campingbenin/confirmation_paiement.html')

def create_temoignage(request):
    return render(request, 'Campingbenin/create_temoignage.html')
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

def create_reservation(request):
    if request.method == 'POST':
        client_name = request.POST.get('name')
        client_email = request.POST.get('mail')
        client_phone = request.POST.get('numeroTelephone')
        size = request.POST.get('size')
        total_amount = request.POST.get('total')
        installments = request.POST.get('installments')
        # Vérifie si 'size' a une valeur valide
        if not size:
            return JsonResponse({'status': 'error', 'message': 'Veuillez sélectionner le nombre de personnes.'})
        # Obtient l'heure actuelle
        current_time = datetime.now().time()  
        current_date = datetime.now()
 
        # Supposons que vous récupérez les données de la réservation depuis le formulaire
        if total_amount == '0' :
            return redirect('reservation')              
        if size and total_amount and installments:
            size = int(size)
            total_amount = Decimal(total_amount)
            installments = int(installments)
            if installments > 1:
                installment_amount = total_amount / installments
                payment_status = "En cours"  # Définir le statut de paiement sur "En cours" par défaut
                # Enregistrer la réservation dans la base de données avec le statut de paiement initial
                reservation = Reservation.objects.create(
                    client_name=client_name,
                    client_email=client_email,
                    client_phone=client_phone,
                    date=current_date,
                    time=current_time,
                    party_size=size,
                    total_amount=total_amount,
                    payment_status=payment_status,
                    installment_amount=installment_amount  # Ajouter le champ installment_amount
                )
                # Effectuer ici les étapes nécessaires pour rediriger vers l'API de KKIApy avec l'information sur le montant de chaque tranche
                # Après chaque paiement de tranche, mettez à jour le statut de paiement
                # Supposons que vous recevez une notification de paiement réussi avec le montant de la tranche
                paid_installment_amount = 50.0  # Supposons que la première tranche de 50 a été payée
                remaining_installments = installments - 1
                if remaining_installments > 0:
                    payment_status = f"Reste {remaining_installments} tranche(s)"
                else:
                    payment_status = "Effectué"
                # Mettre à jour le statut de paiement dans la base de données
                reservation.payment_status = payment_status
                reservation.save()
                # Effectuez ici d'autres actions en fonction du statut de paiement
            else:
                payment_status = "Effectué"  # Si un seul paiement, le statut sera "Effectué"
                # Enregistrer la réservation dans la base de données avec le statut de paiement "Effectué"
                reservation = Reservation.objects.create(
                    client_name=client_name,
                    client_email=client_email,
                    client_phone=client_phone,
                    date=current_date,
                    time=current_time,
                    party_size=size,
                    total_amount=total_amount,
                    payment_status=payment_status,
                    installment_amount=total_amount  # Si un seul paiement, le montant de l'acompte est égal au montant total
                )

        else:         
            # Gérer les erreurs ou les cas où les valeurs ne sont pas définies correctement
             return redirect('reservation')
            #return JsonResponse({'status': 'error', 'message': 'Veuillez remplir tous les champs requis.'})
        # Redirige l'utilisateur vers la page de récapitulatif de réservation
        return redirect('confirmation_reservation', reservation_id=reservation.id)
    else:
        return JsonResponse({'status': 'error'})

def confirmation_reservation(request, reservation_id):
    
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'Campingbenin/confirmation_reservation.html', {'reservation': reservation})

# Classe pour générer les données du ticket
class TicketGenerator:
    def __init__(self):
        self.tent_counter = 1
        self.ticket_counter = 1
    
    def generate_ticket_data(self):
        tent_number = self.tent_counter
        ticket_number = self.ticket_counter
        
        # Augmenter les compteurs pour la prochaine réservation
        self.tent_counter += 1
        self.ticket_counter += 1
        
        return {
            "tent_number": tent_number,
            "ticket_number": ticket_number,
        }

# Fonction pour générer le code QR
def generate_qr_code(reservation_id, tent_number, ticket_number):
    qr_data = f"ID de réservation: {reservation_id}\nNuméro de tente: {tent_number}\nNuméro de ticket: {ticket_number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image

# Fonction pour rendre le PDF à partir du modèle
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

class GeneratePdf(View):
    def get(self, request, reservation_id, *args, **kwargs):
        def get(self, request, reservation_id, *args, **kwargs):
            try:
                reservation = Reservation.objects.get(pk=reservation_id)  # Récupérer la réservation en fonction de l'ID
            except Reservation.DoesNotExist:
             return HttpResponse("Réservation non trouvée")

        # Calculer le numéro de tente en fonction des réservations existantes
        total_reservations = Reservation.objects.count()
        tent_number = f"{total_reservations + 1:03}"  # Format comme 001, 002, etc.

        # Obtenir la date actuelle
        current_date = timezone.now().strftime("%d/%m/%Y")
        # ...
        qr_img = generate_qr_code(reservation_id, tent_number, tent_number)

        # Convertir l'image PIL en base64
        qr_img_buffer = BytesIO()
        qr_img.save(qr_img_buffer, format="PNG")
        qr_img_base64 = base64.b64encode(qr_img_buffer.getvalue()).decode("utf-8")

        data = {
            "reservation": reservation,
            "tent_number": tent_number,
            "current_date": current_date,
            "qr_img_base64": qr_img_base64,  # Utiliser cette variable dans le modèle
        }
        pdf = render_to_pdf('Campingbenin/ticket_template.html', data)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Ticket_Reservation_{reservation_id}.pdf"
            content = f"inline; filename= {filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Échec de la génération du PDF")

def paiement_retour(request, reservation_id):
    # ... (votre code de vérification de paiement et récupération de la réservation)
    transaction_id = request.GET.get('transaction_id')
    k = Kkiapay('25ffe3b0e4f911ed9cc1f1b54a528cb5', 'tpk_26000ac1e4f911ed9cc1f1b54a528cb5', 'tsk_26000ac2e4f911ed9cc1f1b54a528cb5', sandbox="True")
    transaction = k.verify_transaction(transaction_id)

    reservation = Reservation.objects.get(pk=reservation_id)
    if transaction['status'] == 'SUCCESS':
        return render(request, 'Campingbenin/reservation_pass.html', {'reservation': reservation})
    else:
        # ... (votre code en cas d'échec de paiement)
        return redirect('erreur_paiement')


def load_testimonials(request):
    testimonials = Testimonial.objects.order_by('-id')
    paginator = Paginator(testimonials, 5)  # Modifier ici si vous souhaitez une pagination différente, ex: 10 témoignages par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Campingbenin/create_temoignage.html', {'page_obj': page_obj})
  
def create_testimonial(request):
        if request.method == 'POST':
             author = request.POST.get('authorName')
             text = request.POST.get('testimonyText')

         # Enregistrement du témoignage
             testimonial = Testimonial.objects.create(author=author, text=text)
             testimonial.save
             return redirect('load_testimonials')
        else:
            return render(request, 'create_temoignage.html')
