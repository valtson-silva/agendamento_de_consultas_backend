import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from professionals.models.professionals import Professionals


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
def test_professional_create():
    client = APIClient()
    url = reverse("professionals-list")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    
    response = client.post(url,
        {
            "name": "joão",
            "email": "joao@email.com",
            "password": "1111111",
            "address": "Rua de teste",
            "phone": "9999999999"
        },
        format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == "joão"
    

@pytest.mark.django_db
def test_professional_list():
    client = get_authenticated_client()
    url = reverse("professionals-list")
    
    response = client.get(url)
    
    assert response.status_code == 200


@pytest.mark.django_db
def test_professional_retrieve():
    client = get_authenticated_client()
    professional = Professionals.objects.create(
        name="Carlos", email="carlos@email.com", password="senha",
        address="Rua B", phone="888888888"
    )
    
    url = reverse("professionals-detail", args=[professional.id])
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data["name"] == "Carlos"
    

@pytest.mark.django_db
def test_professional_update():
    client = get_authenticated_client_permission()
    professional = Professionals.objects.create(
        name="Ana", email="ana@email.com", password="senha",
        address="Rua C", phone="777777777"
    )
    url = reverse("professionals-detail", args=[professional.id])
    data = {
        "name": "Ana Paula",
        "email": "ana@email.com",
        "password": "senha",
        "address": "Rua C Atualizada",
        "phone": "777777777"
    }
    
    response = client.put(url, data, format="json")
    
    assert response.status_code == 200
    assert response.data["name"] == "Ana Paula"
    
    
@pytest.mark.django_db
def test_professional_partial_update():
    client = get_authenticated_client_permission()
    professional = Professionals.objects.create(
        name="Pedro", email="pedro@email.com", password="senha",
        address="Rua D", phone="666666666"
    )
    url = reverse("professionals-detail", args=[professional.id])
    
    response = client.patch(url, {"phone": "000000000"}, format="json")
    
    assert response.status_code == 200
    assert response.data["phone"] == "000000000"
    

@pytest.mark.django_db
def test_professional_delete():
    client = get_authenticated_client_permission()
    professional = Professionals.objects.create(
        name="Luiza", email="luiza@email.com", password="senha",
        address="Rua E", phone="555555555"
    )
    user = User.objects.create_user(
        username="Luiza",
        password="senha",
        email="luiza@email.com"
    )
    
    url = reverse("professionals-detail", args=[professional.id])
    response = client.delete(url)
    
    assert response.status_code == 204
    assert not Professionals.objects.filter(id=professional.id).exists()
    