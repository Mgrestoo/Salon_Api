from rest_framework import serializers
from salon.models import  Service, Stylist, Customer, Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','password','email']
        
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
            
        )

class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields = ['id','name','price','duration']
    
    
class StylistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Stylist
        fields = ['id','username','email','bio','services','created_at']
        read_only_fields = ['id','created_at']                
 

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True) 
    
    class Meta:
        model = Customer
        fields = ['id','username','email','phone','created_at']
        read_only_fields = ['id','created_at']
        
    def validate_phone(self, value):
        if not value:
            return value
        
        value = value.strip()
        
        if not value.startswith('+'):
            raise serializers.ValidationError(
                'Phone number should start with + e.g (+2547123456878)'    
            )
        if len(value) < 10:
            raise serializers.ValidationError('Phone number is too short')
        
        if not value[1:].isdigit():
            raise serializers.ValidationError(
                'Phone number should only contain numbers after +'
            )  
        
        return value    
          

class AppointmentSerializer(serializers.ModelSerializer):
    
    customer = CustomerSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    stylist = StylistSerializer(read_only=True)
    
    
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only= True
    )
    
    stylist_id = serializers.PrimaryKeyRelatedField(
        queryset = Stylist.objects.all(),
        source = 'stylist',
        write_only = True
    )
    
    service_id = serializers.PrimaryKeyRelatedField(
        queryset = Service.objects.all(),
        source = 'stylist',
        write_only = True
    )
    
    class Meta:
        model = Appointment
        fields = ['id',
                  
                  'customer','stylist','service',
                  
                  'customer_id','stylist_id','service_id',
                      
                  'due_date','status','notes','created_at'
                  
                  ]
        read_only_fields = ['id','created_at']   
        
        
    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Appointment date cannot be in the past'
            )
        return value             