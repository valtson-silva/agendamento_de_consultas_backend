from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Professionals
from .serializers import ProfessionalSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class ProfessionalCreateView(APIView):
    # Salva um profissional no banco de dados
    
    def post(self, request):
        # Serializa os dados recebidos no corpo da requisição
        serializer = ProfessionalSerializer(data=request.data)
        
        # Verifica se é válido
        if serializer.is_valid():
            # Salva o profissional no banco de dados
            serializer.save()
            
            # Cria o usuário com a senha criptografada
            User.objects.create_user(
                username=request.data["name"],
                password=request.data["password"],
                email=request.data["email"]
            )
            
            # Retorna o profissional salvo e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            
            # Retorna error e o status 400
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
     
     
class ProfessionalListView(APIView):
    # Mostra todos os profissionais salvos no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtém todos os profissional
        professionals = Professionals.objects.all()
        # Serializa os profissionais
        serializer = ProfessionalSerializer(professionals, many=True)
        # Retorna todos os profissionais e o status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProfessionalDetailView(APIView):
    # Mostra os detalhes de um profissional que está no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            # Tenta obter o profissional
            professional = Professionals.objects.get(id=id)
            # Serializa o profissional
            serializer = ProfessionalSerializer(professional)
            # Retorna o profissional
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class ProfessionalUpdateView(APIView):
    # Atualiza os dados de um profissional
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            # Tenta obter o profissional
            professional = Professionals.objects.get(id=id)
            # Serializa os dados recebidos no corpo da requisição
            serializer = ProfessionalSerializer(professional, data=request.data)
            
            # Obtém o usuário pelo email
            user = User.objects.get(email=professional.email)
            # Faz as alterações no usuário
            user.username = request.data.get("name")
            user.password = make_password(request.data.get("password"))
            user.email = request.data.get("email")
            
            # Verifica se os dados são válidos
            if serializer.is_valid():
                # Salva as alterações no banco de dados
                serializer.save()
                user.save()
                
                # Retorna os dados atualizados do profissional e o status 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                
                # Retorna error e o staus 400
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            
            # Retorna error e o status 404
            return Response({"error": "Não existe um prosissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class ProfessionalDeleteView(APIView):
    # Deleta um profissional do banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            # Tenta obter o profissional
            professional = Professionals.objects.get(id=id)
            # Tenta obter o usuário
            user = User.objects.get(email=professional.email)
            # Deleta o profissional do banco de dados
            professional.delete()
            # Deleta o usuário do banco de dados
            user.delete()
            
            # Retorna sucesso e o status 200
            return Response({"success": "Profissional deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            
            # Retorna error e o status 404
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        