from django.contrib.auth.models import User, Group, Permission
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from professionals.models.professionals import Professionals
from professionals.serializers import ProfessionalSerializer


def create_professionals_with_user(data):
    with transaction.atomic():
        serializer = ProfessionalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        try:
            user = User.objects.create_user(
                username=data["name"],
                password=data["password"],
                email=data["email"]
            )
            
            group = Group.objects.get(name="Professionals")
            user.groups.add(group)
        except Exception as e:
            raise ValueError(f"Erro ao criar profissional e usuário: {str(e)}")
    
    return serializer.data


def delete_profissional_with_user(id):
    try:
        profissional = Professionals.objects.get(id=id)
        user = User.objects.get(email=profissional.email)
    except ObjectDoesNotExist:
        raise ValueError("Profissional não encontrado")
    
    profissional.delete()
    user.delete()
    return "Profissional deletado com sucesso"
