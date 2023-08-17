from django import forms
from .models import Event
from .models import Reservation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'price', 'capacity', 'location']




class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client_name', 'client_email', 'client_phone', 'date', 'time', 'party_size', 'total_amount', 'cancellation_policy']
