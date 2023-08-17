"""
Campingbenin URL Configuration

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
from django.urls import path
from camping import views
from django.contrib import admin
from camping.views import event_list_view, create_reservation,  GeneratePdf


# ReservationPDFView,

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('create_temoignage/', views.create_temoignage, name='create_temoignage'),
    path('reservation_pass/', views.reservation_pass, name='reservation_pass'),
    path('erreur_paiement/', views.erreur_paiement, name='erreur_paiement'),
    path('confirmation_paiement/', views.confirmation_paiement, name='confirmation_paiement'),
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
    path('paiement_retour/<int:reservation_id>/', views.paiement_retour, name='paiement_retour'),
    path('create_testimonial/', views.create_testimonial, name='create_testimonial'),
    path('load_testimonials/', views.load_testimonials, name='load_testimonials'),
    # path('telecharger_pdf/<int:reservation_id>/', views.telecharger_pdf, name='telecharger_pdf'),
    # path('pdf/<int:reservation_id>/', TicketPDFView.as_view(), name='pdf'),
    # path('telpdf/<int:reservation_id>/', ReservationPDFView.as_view(), name='telpdf'),
    # path('reservation_passes/<int:reservation_id>/', views.reservation_passes, name='reservation_passes'),
   
    # path('pdf/', GeneratePdf.as_view(),name='pdf'), 
    path('pdf/<int:reservation_id>/', GeneratePdf.as_view(), name='generate_pdf'),



]
