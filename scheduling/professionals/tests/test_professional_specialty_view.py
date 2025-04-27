import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from professionals.models import Professionals, Specialty, ProfessionalSpecialty
from rest_framework.authtoken.models import Token

def create_professional():
    return Professionals.objects.create(
        name="João",
        email="joao@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_specialty():
    return Specialty.objects.create(
        name="Cardiologia"
    )
    
def create_professional_specialty():
    specialty = create_specialty()
    professional = create_professional()
    
    return ProfessionalSpecialty.objects.create(
        specialty=specialty,
        professional=professional
    )

@pytest.mark.django_db
def test_professional_specialty_create():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("professional_specialty_create")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    specialty = create_specialty()
    professional = create_professional()
    
    response = client.post(url, {
        "specialty": specialty.id,
        "professional": professional.id
    })
    
    assert response.status_code == 201
    

@pytest.mark.django_db
def test_professional_specialty_list():
    # Testa obter todas as especialidades de um profissional
    
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    professionalSpecialty = create_professional_specialty()
    url = reverse("professional_specialty_list", args=[professionalSpecialty.professional.id])
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_specialty_professional_list():
    # Testa obter todos os profissionais de uma especialidade
    
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    professionalSpecialty = create_professional_specialty()
    url = reverse("specialty_professional_list", args=[professionalSpecialty.specialty.id])
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
    