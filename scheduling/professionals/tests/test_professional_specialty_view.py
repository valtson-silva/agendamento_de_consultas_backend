import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from professionals.models import Professionals, Specialty, ProfessionalSpecialty

def create_professional():
    # Cria um profissional
    return Professionals.objects.create(
        name="João",
        email="joao@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_specialty():
    # Cria uma especialidade
    return Specialty.objects.create(
        name="Cardiologia"
    )
    
def create_professional_specialty():
    # Cria um registro
    
    specialty = create_specialty()
    professional = create_professional()
    
    return ProfessionalSpecialty.objects.create(
        specialty=specialty,
        professional=professional
    )

@pytest.mark.django_db
def test_professional_specialty_create():
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Obtém a url
    url = reverse("professional_specialty_create")
    # Faz o login
    client.login(username="testuser", password="testpass")
    
    # Cria a especialidade e o profissional
    specialty = create_specialty()
    professional = create_professional()
    # Faz a requisição post
    response = client.post(url, {
        "specialty": specialty.id,
        "professional": professional.id
    })
    # Verifica se o status retornado foi 201 created
    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_specialty_list():
    # Testa obter todas as especialidades de um profissional
    
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Cria um registro
    professionalSpecialty = create_professional_specialty()
    # Obtém a url
    url = reverse("professional_specialty_list", args=[professionalSpecialty.professional.id])
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_specialty_professional_list():
    # Testa obter todos os profissionais de uma especialidade
    
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Cria um registro
    professionalSpecialty = create_professional_specialty()
    # Obtém a url
    url = reverse("specialty_professional_list", args=[professionalSpecialty.specialty.id])
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    