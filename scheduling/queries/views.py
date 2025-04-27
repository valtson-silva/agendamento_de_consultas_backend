from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuerySerializer
from .models import Queries
from professionals.views_professionals import PermissionForProfessionals

class QueryCreateView(APIView):
    # Salva uma consulta no banco de dados
    
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class QueriesListView(APIView):
    # Mostra todos as consultas salvas no banco de dados
    
    permission_classes = [PermissionForProfessionals]
    
    def get(self, request):
        queries = Queries.objects.all()
        serializer = QuerySerializer(queries, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QueryDetailView(APIView):
    # Mostra os detalhes de uma consulta que está no banco de dados
    
    def get(self, request, id):
        try:
            query = Queries.objects.get(id=id)
            serializer = QuerySerializer(query)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class QueryUpdateView(APIView):
    # Atualiza os dados de uma consulta
    
    def put(self, request, id):
        try:
            query = Queries.objects.get(id=id)
            serializer = QuerySerializer(query, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class QueryDeleteView(APIView):
    # Deleta uma consulta do banco de dados
    
    def delete(self, request, id):
        try:
            query = Queries.objects.get(id=id)
            query.delete()
            
            return Response({"success": "Consulta deletada com sucesso."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class QueryProfessionalListView(APIView):
    # Mostra todas as consultas referentes a um profissional
    
    permission_classes = [PermissionForProfessionals]
    
    def get(self, request, professional_id):
        try:
            queries = Queries.objects.filter(professional=professional_id)
            serializer = QuerySerializer(queries, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe existe consulta com esse profissional."}, status=status.HTTP_404_NOT_FOUND)

class QueryPatientListView(APIView):
    # Mostra todas as consultas referentes a um paciente
    
    def get(self, request, patient_id):
        try:
            queries = Queries.objects.filter(patient=patient_id)
            serializer = QuerySerializer(queries, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe existe consulta com esse paciente."}, status=status.HTTP_404_NOT_FOUND)
        
class QuerySpecialtyListView(APIView):
    # Mostra todas as consultas referentes a uma especialidade
    
    permission_classes = [PermissionForProfessionals]
    
    def get(self, request, specialty_id):
        try:
            queries = Queries.objects.filter(specialty=specialty_id)
            serializer = QuerySerializer(queries, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe existe consulta com essa especialidade."}, status=status.HTTP_404_NOT_FOUND)
            