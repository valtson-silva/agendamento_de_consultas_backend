from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuerySerializer
from .models import Queries

class QueryCreateView(APIView):
    # Salva uma consulta no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Serializa os dados recebidos no corpo da requisição
        serializer = QuerySerializer(data=request.data)
        
        # Verifica se é válido
        if serializer.is_valid():
            # Salva a consulta no banco de dados
            serializer.save()
            
            # Retorna a consulta salva e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            
            # Retorna error e o status 400
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class QueriesListView(APIView):
    # Mostra todos as consultas salvas no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtém todas as consultas
        queries = Queries.objects.all()
        # Serializa as consultas
        serializer = QuerySerializer(queries, many=True)
        # Retorna todas as consultas e o status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QueryDetailView(APIView):
    # Mostra os detalhes de uma consulta que está no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            # Tenta obter a consulta
            query = Queries.objects.get(id=id)
            # Serializa a consulta
            serializer = QuerySerializer(query)
            
            # Retorna a query e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class QueryUpdateView(APIView):
    # Atualiza os dados de uma consulta
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            # Tenta obter uma consulta pelo ID
            query = Queries.objects.get(id=id)
            # Serializa as alterações
            serializer = QuerySerializer(query, data=request.data)
            # Verifica se os dados são válidos
            if serializer.is_valid():
                # Salva as alterações no banco de dados
                serializer.save()
                
                # Retorna a consulta e o status 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Retorna error e o status 400
                return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class QueryDeleteView(APIView):
    # Deleta uma consulta do banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            # Tenta obter a consulta
            query = Queries.objects.get(id=id)
            # Deleta a consulta
            query.delete()
            
            # Retorna sucesso e o status 200
            return Response({"success": "Consulta deletada com sucesso."}, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe uma consulta com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class QueryProfessionalListView(APIView):
    # Mostra todas as consultas referentes a um profissional
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, professional_id):
        try:
            # Tenta obter todas as consultas de um profissional
            queries = Queries.objects.filter(professional=professional_id)
            # Serializa todas as consultas
            serializer = QuerySerializer(queries, many=True)
            
            # Retorna todas as consultas e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe existe consulta com esse profissional."}, status=status.HTTP_404_NOT_FOUND)

class QueryPatientListView(APIView):
    # Mostra todas as consultas referentes a um paciente
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, patient_id):
        try:
            # Tenta obter todas as consultas de um paciente
            queries = Queries.objects.filter(patient=patient_id)
            # Serializa todas as consultas
            serializer = QuerySerializer(queries, many=True)
            
            # Retorna todas as consultas e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe existe consulta com esse paciente."}, status=status.HTTP_404_NOT_FOUND)
        
class QuerySpecialtyListView(APIView):
    # Mostra todas as consultas referentes a uma especialidade
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, specialty_id):
        try:
            # Tenta obter todas as consultas de uma especialidade
            queries = Queries.objects.filter(specialty=specialty_id)
            # Serializa todas as consultas
            serializer = QuerySerializer(queries, many=True)
            
            # Retorna todas as consultas e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe existe consulta com essa especialidade."}, status=status.HTTP_404_NOT_FOUND)
            