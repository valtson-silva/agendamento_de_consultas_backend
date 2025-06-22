import pytest
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

from queries.models import Queries


date_of_consultation = now() + timedelta(days=2)


@pytest.mark.django_db
def test_query_create(get_authenticated_client, create_patient, create_professional, create_specialty):
    client = get_authenticated_client
    url = reverse("queries-list")
    
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
def test_queries_list(get_authenticated_client_permission):
    client = get_authenticated_client_permission
    url = reverse("queries-list")
    
    response = client.get(url)
    
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_queries_retrieve(get_authenticated_client, create_query):
    client = get_authenticated_client
    query = create_query()
    url = reverse("queries-detail", args=[query.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data["professional"] == query.professional.id
    
    
@pytest.mark.django_db
def test_queries_update(get_authenticated_client, create_query):
    client = get_authenticated_client
    query = create_query()
    url = reverse("queries-detail", args=[query.id])
    data = {
        "patient": query.patient.id,
        "professional": query.professional.id,
        "date_hour": date_of_consultation,
        "status": "agendada",
        "specialty": query.specialty.id,
        "observations": "teste_atualizada"
    }
    
    response = client.put(url, data, format="json")
    
    assert response.status_code == 200
    assert response.data["observations"] == data["observations"]
    

@pytest.mark.django_db
def test_queries_partial_update(get_authenticated_client, create_query):
    client = get_authenticated_client
    query = create_query()
    url = reverse("queries-detail", args=[query.id])
    
    response = client.patch(url, {"observations": "teste_atualizada"}, format="json")
    
    assert response.status_code == 200
    assert response.data["observations"] == "teste_atualizada"
    

@pytest.mark.django_db
def test_queries_delete(get_authenticated_client, create_query):
    client = get_authenticated_client
    query = create_query()
    url = reverse("queries-detail", args=[query.id])
    
    response = client.delete(url)
    
    assert response.status_code == 204
    assert not Queries.objects.filter(id=query.id).exists()
    

@pytest.mark.django_db
def test_queries_professional_list(get_authenticated_client_permission, create_query):
    """Testa obter as consultas de um profissional"""
    
    client = get_authenticated_client_permission
    query = create_query()
    url = reverse("queries-professional-list", args=[query.professional.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data[0]["professional"] == query.professional.id
    
    
@pytest.mark.django_db
def test_queries_patient_list(get_authenticated_client, create_query):
    """Testa obter as consultas de um paciente"""
    
    client = get_authenticated_client
    query = create_query()
    url = reverse("queries-patient-list", args=[query.patient.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data[0]["patient"] == query.patient.id
    
  
@pytest.mark.django_db
def test_queries_specialty_list(get_authenticated_client_permission, create_query):
    """Testa obter as consultas de uma especialidade"""
    
    client = get_authenticated_client_permission
    query = create_query()
    url = reverse("queries-specialty-list", args=[query.specialty.id])
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data[0]["specialty"] == query.specialty.id
      