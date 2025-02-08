import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from professionals.models import Professionals, Specialty
from patients.models import Patients
from queries.models import Queries
from django.utils.timezone import now
from datetime import timedelta

date_of_consultation = now() + timedelta(days=2)

def create_professional():
    # Cria um profissional
    return Professionals.objects.create(
        name="João",
        email="joao@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_patient():
    # Cria um paciente
    return Patients.objects.create(
        name="Alfredo",
        email="alfredo@email.com",
        password="1111111",
        address="Rua de teste",
        phone="99999999"
    )
    
def create_specialty():
    # Cria uma especialidade
    return Specialty.objects.create(
        name="Cardiologia"
    )
    
def create_query():
    # Cria uma query
    
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
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Obtém a url
    url = reverse("query_create")
    # Faz o login
    client.login(username="testuser", password="testpass")
    
    # Cria o paciente, o profissional e a especialidade
    patient = create_patient()
    professional = create_professional()
    specialty = create_specialty()
    
    # Faz a requisição post
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
    
    # Verifica se o status retornado foi 201 created
    assert response.status_code == 201
    
    
@pytest.mark.django_db
def test_queries_list():
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Obtém a url
    url = reverse("queries_list")
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_queries_professional_list():
    # Testa obter as consultas de um profissional
    
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Cria a consulta
    query = create_query()
    # Obtém a url
    url = reverse("queries_professional_list", args=[query.professional.id])
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_queries_patient_list():
    # Testa obter as consultas de um paciente
    
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Cria a consulta
    query = create_query()
    # Obtém a url
    url = reverse("queries_patient_list", args=[query.patient.id])
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
    
  
@pytest.mark.django_db
def test_queries_specialty_list():
    # Testa obter as consultas de uma especialidade
    
    # Simula um cliente HTTP
    client = APIClient()
    # Cria um usuário de teste
    user = User.objects.create_user(username="testuser", password="testpass")
    # Cria a consulta
    query = create_query()
    # Obtém a url
    url = reverse("queries_specialty_list", args=[query.specialty.id])
    # Faz o login
    client.login(username="testuser", password="testpass")
    # Faz a requisição get
    response = client.get(url)
    # Verifica se o status retornado foi 200 OK
    assert response.status_code == 200
      