from .models import Appointment, Customer, Service, Stylist
from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, ServiceSerializer, StylistSerializer, CustomerSerializer, AppointmentSerializer)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

User = get_user_model() 

class RegisterAPIView(CreateAPIView):
    @extend_schema(
    summary = 'Register a new user',
    description = '''
    Creates a new user account.
    Returns the user id and username.
    Password is never returned in the response.
    ''',
    responses={201:RegisterSerializer},
    tags=['Authentication'],
    )
    
    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
 
class ServiceViewSet(ModelViewSet):
    @extend_schema(tags=['Services'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Services'],
        summary='Create a new service',
        description='Admin only. Creates a new salon service with name, price and duration.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Service.objects.all().order_by('price')
    
class CustomerViewSet(ModelViewSet):
    @extend_schema(
        tags=['Customers'],
        summary='Create customer profile',
        description='''
        Creates a customer profile for the logged in User
        Only one profile per user allowed
        User is automatically linked - No need to send user_id
        ''',
        examples=[
            OpenApiExample(
                'Create customer profile',
                value={'phone':'+254712345678'},
                request_only=True,
            )
        ]
        
    )
    def create(self,request,*args,**kwargs):
        return super().create(request,*args,**kwargs)
    
    @extend_schema(tags=['Customers'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.select_related('user').filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StylistViewSet(ModelViewSet):
    @extend_schema(tags=['Stylists'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Stylists'],
        summary='Create stylist profile',
        description='''
            Creates a stylist profile for the logged in user.
            Optionally assign services the stylist offers.
        ''',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    serializer_class = StylistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Stylist.objects.select_related('user').prefetch_related('services').all() 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    

class AppointmentViewSet(ModelViewSet):
    @extend_schema(
        tags=['Appointments'],
        summary='List Appointments',
        description='''
        Returns appointments relevant to the logged in user.
        Customers see their own bookings.
        Stylists see their assigned appointments.
        Filtered automatically — no extra parameters needed.
        ''',   
    )
    def list(self,requests,*args,**kwargs):
        return super().list(requests,*args,**kwargs)
    @extend_schema(
        tags=['Appointments'],
        summary='Create appointment',
        description='''
            Books a new appointment.
            Customer is automatically set from the logged in user.
            Send stylist_id, service_id, due_date and optional notes.
        ''',
        examples=[
            OpenApiExample(
                'Book appointment',
                value={
                    'stylist_id': 1,
                    'service_id': 1,
                    'due_date':   '2026-12-01',
                    'notes':      'Please use organic products'
                },
                request_only=True,
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        return Appointment.objects.select_related('customer__user', 'stylist__user','service').filter(
            Q(customer__user=self.request.user)| Q(stylist__user=self.request.user)
        ).distinct()
    
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)
        
    
    