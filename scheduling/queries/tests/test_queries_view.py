import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from professionals.models import Professionals, Specialty
from patients.models import Patients
from queries.models import Queries
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.authtoken.models import Token

date_of_consultation = now() + timedelta(days=2)

def create_professional():
    return Professionals.objects.create(
        name="João",
        email="joao@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_patient():
    return Patients.objects.create(
        name="Alfredo",
        email="alfredo@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_specialty():
    return Specialty.objects.create(
        name="Cardiologia"
    )
    
def create_query():
    professional = create_professional()
    specialty = create_specialty()
    patient = create_patient()
    
    return Queries.objects.create(
        patient=patient,
        specialty=specialty,
        professional=professional,
        date_hour=date_of_consultation,
        status="agendada",
        observations="teste"
    )


@pytest.mark.django_db
def test_query_create():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("query_create")
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token "+ token.key)
    
    patient = create_patient()
    professional = create_professional()
    specialty = create_specialty()
    
    response = client.post(url,
        {
            "patient": patient.id,
            "professional": professional.id,
            "date_hour": date_of_consultation,
            "status": "agendada",
            "specialty": specialty.id,
            "observations": "teste"
        }
    )
    
    assert response.status_code == 201
    
    
@pytest.mark.django_db
def test_queries_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("queries_list")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_queries_professional_list():
    # Testa obter as consultas de um profissional
    
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    query = create_query()
    url = reverse("queries_professional_list", args=[query.professional.id])
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_queries_patient_list():
    # Testa obter as consultas de um paciente
    
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    query = create_query()
    url = reverse("queries_patient_list", args=[query.patient.id])
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
    
  
@pytest.mark.django_db
def test_queries_specialty_list():
    # Testa obter as consultas de uma especialidade
    
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    query = create_query()
    url = reverse("queries_specialty_list", args=[query.specialty.id])
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
    
    assert response.status_code == 200
      