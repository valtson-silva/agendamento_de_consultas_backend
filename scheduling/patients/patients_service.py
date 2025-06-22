from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import transaction

from .models import Patients
from .serializers import PatientsSerializer


def create_patient_with_user(data):
    with transaction.atomic():
        serializer = PatientsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        try:
            user = User.objects.create_user(
                username=data["name"],
                password=data["password"],
                email=data["email"]
            )
        except Exception as e:
            raise ValueError(f"Erro ao criar paciente e usuário: {str(e)}")
    
    return serializer.data


def delete_patient_with_user(id):
    try:        
        patient = Patients.objects.get(id=id)
        user = User.objects.get(email=patient.email)
    except ObjectDoesNotExist:
        raise ValueError("Paciente não encontrado")
    
    patient.delete()
    user.delete()
    return "Paciente deletado com sucesso"
