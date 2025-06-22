import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from professionals.models.specialties import Specialties


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


@pytest.mark.django_db
def test_specialty_create():
    client = get_authenticated_client_permission()
    url = reverse("specialties-list")
    
    response = client.post(url,
        {
            "name": "Cardiologia"
        },
        format="json"
    )

    assert response.status_code == 201
    

@pytest.mark.django_db
def test_specialty_list():
    client = get_authenticated_client()
    url = reverse("specialties-list")
    
    response = client.get(url)
   
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_specialty_retrieve():
    client = get_authenticated_client()
    specialty = Specialties.objects.create(
        name="Psiquiatra"
    )
    
    url = reverse("specialties-detail", args=[specialty.id])
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data["name"] == "Psiquiatra"
    
    
@pytest.mark.django_db
def test_specialty_update():
    client = get_authenticated_client_permission()
    specialty = Specialties.objects.create(
        name="Pediatra"
    )
    
    url = reverse("specialties-detail", args=[specialty.id])
    data = {
        "name": "Ortopedia"
    }
    
    response = client.put(url, data, format="json")
    
    assert response.status_code == 200
    assert response.data["name"] == "Ortopedia"
    
    
@pytest.mark.django_db
def test_specialty_partial_update():
    client = get_authenticated_client_permission()
    specialty = Specialties.objects.create(
        name="Neurologista"
    )
    
    url = reverse("specialties-detail", args=[specialty.id])
    response = client.patch(url, {"name": "Oftalmologista"}, format="json")
    
    assert response.status_code == 200
    assert response.data["name"] == "Oftalmologista"
    
    
@pytest.mark.django_db
def test_specialty_delete():
    client = get_authenticated_client_permission()
    specialty = Specialties.objects.create(
        name="Endocrinologista"
    )
    
    url = reverse("specialties-detail", args=[specialty.id])
    response = client.delete(url)
    
    assert response.status_code == 204
    assert not Specialties.objects.filter(id=specialty.id)
    