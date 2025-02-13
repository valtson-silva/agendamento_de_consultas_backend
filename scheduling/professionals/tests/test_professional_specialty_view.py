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
    
    url = reverse("professional_specialty_create")
    
    client.login(username="testuser", password="testpass")
    
    
    specialty = create_specialty()
    professional = create_professional()
    
    response = client.post(url, {
        "specialty": specialty.id,
        "professional": professional.id
    })
    # Verifica se o status retornado foi 201 created
    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_specialty_list():
    # Testa obter todas as especialidades de um profissional
    
    
    client = APIClient()
    
    user = User.objects.create_user(username="testuser", password="testpass")
    
    professionalSpecialty = create_professional_specialty()
    
    url = reverse("professional_specialty_list", args=[professionalSpecialty.professional.id])
    
    client.login(username="testuser", password="testpass")
    
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_specialty_professional_list():
    # Testa obter todos os profissionais de uma especialidade
    
    
    client = APIClient()
    
    user = User.objects.create_user(username="testuser", password="testpass")
    
    professionalSpecialty = create_professional_specialty()
    
    url = reverse("specialty_professional_list", args=[professionalSpecialty.specialty.id])
    
    client.login(username="testuser", password="testpass")
    
    response = client.get(url)
    
    assert response.status_code == 200
    
