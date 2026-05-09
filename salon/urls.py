from django.urls import path
from .views import RegisterAPIView, AppointmentViewSet, ServiceViewSet, StylistViewSet, CustomerViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r'appointment', AppointmentViewSet, basename='appointment')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'stylist', StylistViewSet, basename='stylist')
router.register(r'service', ServiceViewSet, basename='service')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    
    # JWT ENDPOINTS
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh')
    
] + router.urls
