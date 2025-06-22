import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from django.utils.timezone import now
from datetime import timedelta

from professionals.models.professionals import Professionals
from professionals.models.specialties import Specialties
from patients.models import Patients
from queries.models import Queries


@pytest.fixture
def get_authenticated_client():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
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


@pytest.fixture
def create_patient(db):
    def make_patient(**kwargs):
        data = {
            "name": "Alfredo",
            "email": "alfredo@email.com",
            "password": "1111111",
            "address": "Rua de teste",
            "phone": "99999999"
        }
        data.update(kwargs)
        return Patients.objects.create(**data)
    return make_patient


@pytest.fixture
def create_professional(db):
    def make_professional(**kwargs):
        data = {
            "name": "João",
            "email": "joao@email.com",
            "password": "1111111",
            "address": "Rua de teste",
            "phone": "99999999"
        }
        data.update(kwargs)
        return Professionals.objects.create(**data)
    return make_professional


@pytest.fixture
def create_specialty(db):
    def make_specialty(**kwargs):
        data = {
            "name": "Cardiologia"
        }
        data.update(kwargs)
        return Specialties.objects.create(**data)
    return make_specialty


@pytest.fixture
def create_query(create_patient, create_professional, create_specialty, db):
    def make_query():
        patient = create_patient()
        professional = create_professional()
        specialty = create_specialty()
        date_hour = now() + timedelta(days=2)

        return Queries.objects.create(
            patient=patient,
            professional=professional,
            specialty=specialty,
            date_hour=date_hour,
            status="agendada",
            observations="teste"
        )
    return make_query
