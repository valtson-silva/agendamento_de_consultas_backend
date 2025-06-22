from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin

from professionals.serializers import ProfessionalSpecialtySerializer
from professionals.models.professional_specialty import ProfessionalSpecialty
from .professionals_views import PermissionForProfessionals
from professionals.services.professional_specialty_service import get_professional_specialties, get_specialty_professionals


class MyCreateUpdateDeleteView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    permission_classes = [PermissionForProfessionals]
    
    queryset = ProfessionalSpecialty.objects.all()
    serializer_class = ProfessionalSpecialtySerializer
    
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

        
class ProfessionalSpecialtyListView(APIView):
    """Mostra todas as especialidades de um profissional"""
    
    def get(self, request, professional_id):
        try:
            specialties = get_professional_specialties(professional_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(specialties, status=status.HTTP_200_OK)
            
            
class SpecialtyProfessionalListView(APIView):
    """Mostra todos os profissionais de uma especialidade"""
    
    def get(self, request, specialty_id):
        try:
            professionals = get_specialty_professionals(specialty_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(professionals, status=status.HTTP_200_OK)
        