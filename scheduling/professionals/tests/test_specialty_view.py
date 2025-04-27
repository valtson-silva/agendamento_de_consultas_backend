import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
def test_specialty_create():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("specialty_create")
    
    group, created = Group.objects.get_or_create(name="Professionals")
    perm = Permission.objects.get(codename="permission_for_professionals")
    group.permissions.add(perm)
    user.groups.add(group)
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.post(url,
        {
            "name": "Cardiologia"
        }
    )

    assert response.status_code == 201
    

@pytest.mark.django_db
def test_specialty_list():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    url = reverse("specialty_list")
    
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    response = client.get(url)
   
    assert response.status_code == 200
    