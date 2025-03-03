import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_professional_create():
    client = APIClient()
    url = reverse("professional_create")
    
    response = client.post(url,
        {
            "name": "joão",
            "email": "joao@email.com",
            "password": "1111111",
            "address": "Rua de teste",
            "phone": "9999999999"
        }
    )

    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("professionals_list")
    client.login(username="testuser", password="testpass")
    
    response = client.get(url)
    
    assert response.status_code == 200
    