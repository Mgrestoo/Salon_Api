from django.contrib import admin
from .models import Service, Appointment, Customer, Stylist
from django.contrib.auth import get_user_model

User = get_user_model

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user__username','user__email','phone','created_at']

@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ['user__username','user__email','bio','created_at']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer__user__username','stylist__user__username','service__name','service__price','due_date','created_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','price','duration']

