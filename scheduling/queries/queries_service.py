from django.core.exceptions import ObjectDoesNotExist

from professionals.models.professionals import Professionals
from professionals.models.specialties import Specialties
from patients.models import Patients
from .serializers import QuerySerializer


def query_professional(professional_id):
    try:
        professional = Professionals.objects.get(id=professional_id)
    except ObjectDoesNotExist:
        raise ValueError("Profissional não encontrado")
    
    queries = professional.queries.all()
    
    serializer = QuerySerializer(queries, many=True)
    return serializer.data


def query_specialty(specialty_id):
    try:
        specialty = Specialties.objects.get(id=specialty_id)
    except ObjectDoesNotExist:
        raise ValueError("Especialidade não encontrada")
    
    queries = specialty.queries.all()
    serializer = QuerySerializer(queries, many=True)
    return serializer.data


def query_patient(patient_id):
    try:
        patient = Patients.objects.get(id=patient_id)
    except ObjectDoesNotExist:
        raise ValueError("Paciente não encontrado")
    
    queries = patient.queries.all()
    serializer = QuerySerializer(queries, many=True)
    return serializer.data
