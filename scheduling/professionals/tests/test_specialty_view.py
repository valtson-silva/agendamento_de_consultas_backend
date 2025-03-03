import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_specialty_create():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("specialty_create")
    client.login(username="testuser", password="testpass")
    
    response = client.post(url,
        {
            "name": "Cardiologia"
        }
    )

    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("specialty_list")
    client.login(username="testuser", password="testpass")
    
    response = client.get(url)
   
    assert response.status_code == 200
    