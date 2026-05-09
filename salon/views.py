from .models import Appointment, Customer, Service, Stylist
from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, ServiceSerializer, StylistSerializer, CustomerSerializer, AppointmentSerializer)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

User = get_user_model() 

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
 
class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Service.objects.all().order_by('price')
    
class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.select_related('user').filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StylistViewSet(ModelViewSet):
    serializer_class = StylistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Stylist.objects.select_related('user').prefetch_related('services').all() 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    

class AppointmentViewSet(ModelViewSet):
    def get_queryset(self):
        return Appointment.objects.select_related('customer__user', 'stylist__user','service').filter(
            Q(customer__user=self.request.user)| Q(stylist__user=self.request.user)
        ).distinct()
    
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)
        
    
    