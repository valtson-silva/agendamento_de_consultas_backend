import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
def test_patient_create():
    client = APIClient()
    url = reverse("patient_create")
    
    response = client.post(url,
        {
            "name": "joão",
            "email": "joao@email.com",
            "password": "1111111",
            "address": "Rua de teste",
            "phone": "9999999999"
        }
    )
    
    assert response.status_code == 201
    

@pytest.mark.django_db
def test_patient_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    url = reverse("patient_list")
    response = client.get(url)

    assert response.status_code == 200
    