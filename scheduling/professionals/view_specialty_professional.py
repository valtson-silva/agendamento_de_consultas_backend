from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfessionalSpecialtySerializer, SpecialtySerializer, ProfessionalSerializer
from .models import ProfessionalSpecialty
from .views_professionals import PermissionForProfessionals

class ProfessionalSpecialtyCreateView(APIView):
    # Salva essas informações no banco de dados
    
    permission_classes = [PermissionForProfessionals]
        
    def post(self, request):
        serializer = ProfessionalSpecialtySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Os dados informados são inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfessionalSpecialtyListView(APIView):
    # Mostra todas as especialidades de um profissional
    
    def get(self, request, professional_id):
        try:
            # Tenta obter as especialidade de um profissional pelo ID
            specialties = ProfessionalSpecialty.objects.filter(professional=professional_id)
            
            # Lista que recebe as especialidades
            listSpecialty = []
            
            # Itera sobre as especialidades
            for value in specialties:
                listSpecialty.append(value.specialty)
            
            serializer = SpecialtySerializer(listSpecialty, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
            
            
class SpecialtyProfessionalListView(APIView):
    # Mostra todos os profissionais de uma especialidade
    
    def get(self, request, specialty_id):
        try:
            # Tenta obter os profissionais de uma especialidade pelo ID
            professional = ProfessionalSpecialty.objects.filter(specialty=specialty_id)
            
            # Lista que recebe os profissionais
            listProfessional = []
            
            # Itera sobre os profissionais
            for value in professional:
                listProfessional.append(value.professional)
                
            serializer = ProfessionalSerializer(listProfessional, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe uma especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
            
class ProfessionalSpecialtyUpdateView(APIView):
    # Atualiza as informações do registro
    
    permission_classes = [PermissionForProfessionals]
    
    def put(self, request, id):
        try:
            professionalSpecialty = ProfessionalSpecialty.objects.get(id=id)
            serializer = ProfessionalSpecialtySerializer(professionalSpecialty, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe um registro com esse ID."}, status=status.HTTP_404_NOT_FOUND)
      
      
class ProfessionalSpecialtyDeleteView(APIView):
    # Deleta um registro do banco de dados
    
    permission_classes = [PermissionForProfessionals]
    
    def delete(self, request, id):
        try:
            professionalSpecialty = professionalSpecialty.objects.get(id=id)
            professionalSpecialty.delete()
            
            return Response({"success": "Registro deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um registro com esse ID."}, status=status.HTTP_404_NOT_FOUND)  
        