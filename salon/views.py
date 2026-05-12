from .models import Appointment, Customer, Service, Stylist
from django.contrib.auth import get_user_model
from .serializers import (RegisterSerializer, ServiceSerializer, StylistSerializer, CustomerSerializer, AppointmentSerializer)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from drf_spectacular.utils import extend_schema,extend_schema_view, OpenApiParameter, OpenApiExample

User = get_user_model() 
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
class RegisterAPIView(CreateAPIView):    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

@extend_schema_view(
    list=extend_schema(
        summary='List services',
        description='Returns all salon services ordered by price.',
        tags=['Services'],
    ),
    create=extend_schema(
        summary='Create service',
        description='Admin only. Creates a new salon service.',
        tags=['Services'],
        examples=[
            OpenApiExample(
                'Create haircut service',
                value={
                    'name':     'Haircut',
                    'price':    '25.00',
                    'duration': 30,
                },
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(summary='Get service details', tags=['Services']),
    update=extend_schema(summary='Update service', tags=['Services']),
    destroy=extend_schema(summary='Delete service', tags=['Services']),
)
class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Service.objects.all().order_by('price')

@extend_schema_view(
    list=extend_schema(
        summary='List customer profiles',
        description='Returns the customer profile for the logged in user.',
        tags=['Customers'],
    ),
    create=extend_schema(
        summary='Create customer profile',
        description='''
            Creates a customer profile for the logged in user.
            Only one profile per user is allowed.
            User is automatically linked — no need to send user_id.
        ''',
        tags=['Customers'],
        examples=[
            OpenApiExample(
                'Create customer profile',
                value={'phone': '+254799896276'},
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(summary='Get customer profile', tags=['Customers']),
    update=extend_schema(summary='Update customer profile', tags=['Customers']),
    destroy=extend_schema(summary='Delete customer profile', tags=['Customers']),
)    
class CustomerViewSet(ModelViewSet):
    
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.select_related('user').filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary='List stylists',
        description='Returns all stylist profiles with their services.',
        tags=['Stylists'],
    ),
    create=extend_schema(
        summary='Create stylist profile',
        description='''
            Creates a stylist profile for the logged in user.
            Optionally list service IDs the stylist offers.
        ''',
        tags=['Stylists'],
        examples=[
            OpenApiExample(
                'Create stylist profile',
                value={
                    'bio':      '10 years experience in hair styling',
                    'services': [1, 2],
                },
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(summary='Get stylist profile',   tags=['Stylists']),
    update=extend_schema(summary='Update stylist profile',  tags=['Stylists']),
    destroy=extend_schema(summary='Delete stylist profile', tags=['Stylists']),
)
class StylistViewSet(ModelViewSet):
    serializer_class = StylistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Stylist.objects.select_related('user').prefetch_related('services').all() 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    

@extend_schema_view(
    list=extend_schema(
        summary='List appointments',
        description='''
            Returns appointments relevant to the logged in user.
            Customers see their own bookings.
            Stylists see their assigned appointments.
            Filtered automatically — no extra parameters needed.
        ''',
        tags=['Appointments'],
        parameters=[
            OpenApiParameter(
                name='status',
                description='Filter by appointment status',
                required=False,
                type=str,
                enum=['pending', 'confirmed', 'done', 'cancelled'],
            ),
            OpenApiParameter(
                name='ordering',
                description='Order results by field. Use - for descending.',
                required=False,
                type=str,
                enum=['due_date', '-due_date', 'created_at', '-created_at'],
            ),
        ],
    ),
    create=extend_schema(
        summary='Create appointment',
        description='''
            Books a new appointment.
            Customer is automatically set from the logged in user.
            Due date cannot be in the past.
            Confirmation email sent automatically on creation.
        ''',
        tags=['Appointments'],
        examples=[
            OpenApiExample(
                'Book a haircut',
                value={
                    'stylist_id': 1,
                    'service_id': 1,
                    'due_date':   '2026-12-01',
                    'notes':      'Please use organic products',
                },
                request_only=True,
            )
        ],
    ),
    retrieve=extend_schema(
        summary='Get appointment details',
        tags=['Appointments'],
    ),
    update=extend_schema(
        summary='Update appointment',
        tags=['Appointments'],
    ),
    partial_update=extend_schema(
        summary='Update appointment status',
        description='Stylists use this to confirm or mark appointments done.',
        tags=['Appointments'],
        examples=[
            OpenApiExample(
                'Confirm appointment',
                value={'status': 'confirmed'},
                request_only=True,
            ),
            OpenApiExample(
                'Mark as done',
                value={'status': 'done'},
                request_only=True,
            ),
        ],
    ),
    destroy=extend_schema(
        summary='Cancel appointment',
        tags=['Appointments'],
    ),
)
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
        
    
    