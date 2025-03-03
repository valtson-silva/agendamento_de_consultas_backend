from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SpecialtySerializer
from .models import Specialty

class SpecialtyCreateView(APIView):
    # Salva um especialidade no banco de dados 

    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SpecialtySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class SpecialtyListView(APIView):
    # Mostra todas as especialidades salvas no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SpecialtyDetailView(APIView):
    # Mostra os detalhes de uma especialidade
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            specialty = Specialty.objects.get(id=id)
            serializer = SpecialtySerializer(specialty)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
        
class SpecialtyUpdateView(APIView):
    # Atualiza os dados de uma especialidade
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            specialty = Specialty.objects.get(id=id)
            serializer = SpecialtySerializer(specialty, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe uma especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class SpecialtyDeleteView(APIView):
    # Deleta um especialidade do banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            specialty = Specialty.objects.get(id=id)
            specialty.delete()
            
            return Response({"success": "Especialidade deletada com sucesso."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe uma especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        