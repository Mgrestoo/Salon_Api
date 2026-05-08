from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    
    
    def __str__(self):
        return self.username
    

User = get_user_model()

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    
    def __str__(self):
        return f'{self.name} - ${self.price}'
    
class Stylist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stylist_profile')
    bio = models.TextField(blank=True)    
    services = models.ManyToManyField(Service, related_name='stylists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Stylist: {self.user.username}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cutomer_profile')
    phone = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Customer: {self.user.username}'
    

class Appointment(models.Model):
    
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        DONE      = 'done',      'Done'
        CANCELLED = 'cancelled', 'Cancelled'
        
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='appointments')
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    
    
    def __str__(self):
        return f'{self.customer} with {self.stylist} on {self.due_date}'
            