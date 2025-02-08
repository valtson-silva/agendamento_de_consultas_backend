from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SpecialtySerializer
from .models import Specialty

class SpecialtyCreateView(APIView):
    # Salva um especialidade no banco de dados 
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Serializa os dados recebidos no corpo da requisição
        serializer = SpecialtySerializer(data=request.data)
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva a especialidade no banco de dados
            serializer.save()
            # Retorna a especialidade salva e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retorna error e o status 400
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class SpecialtyListView(APIView):
    # Mostra todas as especialidades salvas no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtém todas as especialidades
        specialties = Specialty.objects.all()
        # Serializa todas as especialidades
        serializer = SpecialtySerializer(specialties, many=True)
        # Retorna as especialidadese e o status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SpecialtyDetailView(APIView):
    # Mostra os detalhes de uma especialidade
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            # Tenta obter a especialidade pelo ID
            specialty = Specialty.objects.get(id=id)
            # Serializa a especialidade
            serializer = SpecialtySerializer(specialty)
            
            # Retorna a especialidade e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
        
class SpecialtyUpdateView(APIView):
    # Atualiza os dados de uma especialidade
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            # Tenta obter uma especialidade pelo ID
            specialty = Specialty.objects.get(id=id)
            # Serializa as alterações
            serializer = SpecialtySerializer(specialty, data=request.data)
            # Verifica se os dados são válidos
            if serializer.is_valid():
                # Salva as alterações no banco de dados
                serializer.save()
                
                # Retorna a especialidade e o status 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Retorna error e o status 400
                return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe uma especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class SpecialtyDeleteView(APIView):
    # Deleta um especialidade do banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            # Tenta obter a especialidade
            specialty = Specialty.objects.get(id=id)
            # Deleta a especialidade
            specialty.delete()
            
            # Retorna sucesso e o status 200
            return Response({"success": "Especialidade deletada com sucesso."}, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe uma especialidade com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        