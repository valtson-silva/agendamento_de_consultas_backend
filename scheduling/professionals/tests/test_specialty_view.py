import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_specialty_create():
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Obtém a url
    url = reverse("specialty_create")
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição post
    response = client.post(url,
        {
            "name": "Cardiologia"
        }
    )
    
    # Verifica se o status retornado foi 201 created
    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_list():
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Obtém a url
    url = reverse("specialty_list")
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    