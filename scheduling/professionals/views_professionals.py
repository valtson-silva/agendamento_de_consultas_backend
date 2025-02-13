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
        
        serializer = ProfessionalSerializer(data=request.data)
        
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
            
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
     
     
class ProfessionalListView(APIView):
    # Mostra todos os profissionais salvos no banco de dados
    
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        professionals = Professionals.objects.all()
        
        serializer = ProfessionalSerializer(professionals, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProfessionalDetailView(APIView):
    # Mostra os detalhes de um profissional que está no banco de dados
    

    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            
            professional = Professionals.objects.get(id=id)
            
            serializer = ProfessionalSerializer(professional)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class ProfessionalUpdateView(APIView):
    # Atualiza os dados de um profissional
    
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            
            professional = Professionals.objects.get(id=id)
            
            serializer = ProfessionalSerializer(professional, data=request.data)
            
            # Obtém o usuário pelo email
            user = User.objects.get(email=professional.email)
            # Faz as alterações no usuário
            user.username = request.data.get("name")
            user.password = make_password(request.data.get("password"))
            user.email = request.data.get("email")
            
            
            if serializer.is_valid():
                # Salva as alterações no banco de dados
                serializer.save()
                user.save()
                
                # Retorna os dados atualizados do profissional e o status 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            
            return Response({"error": "Não existe um prosissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class ProfessionalDeleteView(APIView):
    # Deleta um profissional do banco de dados
    
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            
            professional = Professionals.objects.get(id=id)
            
            user = User.objects.get(email=professional.email)
            
            professional.delete()
            
            user.delete()
            
            return Response({"success": "Profissional deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
