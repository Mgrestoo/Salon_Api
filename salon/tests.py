import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Customer, Stylist, Appointment

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='Restoo',
        password='12345678',
        email='restoo@gmail.com'
    )
    
@pytest.fixture   
def authenticated_client(client, user):
    response = client.post(reverse('token_obtain_pair'), {'username':'Restoo','password':'12345678'})   
    
    token = response.data['access']
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}') 
    
    return client

@pytest.mark.django_db
def test_user_can_create_an_account(client):
    
    data = {
        'username':'Restoo',
        'password':'12345678',
        'email':'restoo@gmail.com'
    }
    
    response = client.post(reverse('register'), data)
    
    assert response.status_code == 201
    assert 'password' not in response.data
    assert User.objects.filter(username='Restoo').exists()

@pytest.mark.django_db
def test_user_can_login(client):
    User.objects.create_user(
        username='Restoo',
        password='12345678',
        email='restoo@gmail.com'
    )
    
    data = {
        'username':'Restoo',
        'password':'12345678',
        'email':'restoo@gmail.com'
    }    
    
    response = client.post(reverse('token_obtain_pair'), data)
    
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
        
@pytest.mark.django_db
def test_user_can_create_a_customer_account(authenticated_client, user):
    
    data = {
        'phone':'+254799896276'
    }        
    
    response =authenticated_client.post(reverse('customer-list'), data)
    
    assert Customer.objects.filter(user=user).exists()
    assert response.status_code == 201
    
    customer = Customer.objects.get(user=user)
    assert customer.user == user
    assert customer.phone == '+254799896276'