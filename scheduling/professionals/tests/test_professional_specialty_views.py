import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from professionals.models.professionals import Professionals
from professionals.models.specialties import Specialties
from professionals.models.professional_specialty import ProfessionalSpecialty


def get_authenticated_client():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


def get_authenticated_client_permission():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    return client


def create_professional(email):
    return Professionals.objects.create(
        name="João",
        email=email,
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
    
def create_specialty():
    return Specialties.objects.create(
        name="Cardiologia"
    )
    
    
def create_professional_specialty():
    specialty = create_specialty()
    professional = create_professional("joao@email.com")
    
    return ProfessionalSpecialty.objects.create(
        specialty=specialty,
        professional=professional
    )


@pytest.mark.django_db
def test_professional_specialty_create():
    client = get_authenticated_client_permission()
    url = reverse("professional-specialty-create")
    
    specialty = create_specialty()
    professional = create_professional("joao2@email.com")
    
    response = client.post(url, {
        "specialty": specialty.id,
        "professional": professional.id
    }, format="json")
    
    assert response.status_code == 201
    assert response.data["specialty"] == specialty.id
    

@pytest.mark.django_db
def test_professional_specialty_list():
    """Testa obter todas as especialidades de um profissional"""
    
    client = get_authenticated_client()
    professional_specialty = create_professional_specialty()
    url = reverse("professional-specialties-list", args=[professional_specialty.professional.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data[0]["name"] == "Cardiologia"
    

@pytest.mark.django_db
def test_specialty_professional_list():
    """Testa obter todos os profissionais de uma especialidade"""
    
    client = get_authenticated_client()
    professional_specialty = create_professional_specialty()
    url = reverse("specialty-professionals-list", args=[professional_specialty.specialty.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data[0]["name"] == "João"
    
    
@pytest.mark.django_db
def test_professional_specialty_update():
    client = get_authenticated_client_permission()
    
    professional_specialty = create_professional_specialty()
    professional = create_professional("joao3@email.com")
    
    data = {
        "professional": professional.id,
        "specialty": professional_specialty.specialty.id
    }
    
    url = reverse("professional-specialty-detail", args=[professional_specialty.id])
    response = client.put(url, data, format="json")
    
    assert response.status_code == 200
    assert response.data["professional"] == professional.id
    
    
@pytest.mark.django_db
def test_professional_specialty_delete():
    client = get_authenticated_client_permission()
    professional_specialty = create_professional_specialty()
    
    url = reverse("professional-specialty-detail", args=[professional_specialty.id])
    response = client.delete(url)
    
    assert response.status_code == 204
    assert not ProfessionalSpecialty.objects.filter(id=professional_specialty.id).exists()
    