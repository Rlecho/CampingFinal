from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Reservation(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    party_size = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True) 
    installment_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
         return f"Reservation #{self.id}"

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    location = models.CharField(max_length=100)

class ReservationConfirmation(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    confirmation_number = models.CharField(max_length=50)
    confirmation_date = models.DateTimeField(auto_now_add=True)
    kkia_transaction_code = models.CharField(max_length=100, default=None, null=True)
    status = models.CharField(max_length=50,default=None)
    
class Testimonial(models.Model):
    
    text = models.TextField()
    author = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Temoignage"
        verbose_name_plural = "Temoignages"

    def __str__(self):
        return self.name
    
class ImageObjet(models.Model):
    
    object = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        verbose_name = "Event",
        )
    name = models.CharField(max_length=100, verbose_name = "Titre de l'image")
    image = models.ImageField(upload_to = "event/")
    caption = models.TextField(verbose_name = "Caption", null = True, blank = True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.name