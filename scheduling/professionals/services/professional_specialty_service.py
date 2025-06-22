from django.core.exceptions import ObjectDoesNotExist

from professionals.serializers import SpecialtySerializer, ProfessionalSerializer
from professionals.models.professionals import Professionals
from professionals.models.specialties import Specialties


def get_professional_specialties(professional_id):
    try:
        professional = Professionals.objects.get(id=professional_id)
    except ObjectDoesNotExist:
        raise ValueError("Profissional não encontrado")
    
    specialties = [rel.specialty for rel in professional.specialties.all()]
    
    serializer = SpecialtySerializer(specialties, many=True)
    return serializer.data


def get_specialty_professionals(specialty_id):
    try:
        specialty = Specialties.objects.get(id=specialty_id)
    except ObjectDoesNotExist:
        raise ValueError("Especialidade não encontrada")
    
    professionals = [rel.professional for rel in specialty.professionals.all()]
    
    serializer = ProfessionalSerializer(professionals, many=True)
    return serializer.data
    