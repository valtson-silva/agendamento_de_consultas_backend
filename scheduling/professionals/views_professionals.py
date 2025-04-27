from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny
from .models import Professionals
from .serializers import ProfessionalSerializer
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password

class PermissionForProfessionals(BasePermission):
    # Criação de uma permissão customizada
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.has_perm("professionals.permission_for_professionals"):
            return True
        
        return False

class ProfessionalCreateView(APIView):
    # Salva um profissional no banco de dados
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ProfessionalSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            # Cria o usuário com a senha criptografada
            user = User.objects.create_user(
                username=request.data["name"],
                password=request.data["password"],
                email=request.data["email"]
            )
            group = Group.objects.get(name="Professionals")
            user.groups.add(group)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
     
     
class ProfessionalListView(APIView):
    # Mostra todos os profissionais salvos no banco de dados
    
    def get(self, request):
        professionals = Professionals.objects.all()
        serializer = ProfessionalSerializer(professionals, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProfessionalDetailView(APIView):
    # Mostra os detalhes de um profissional que está no banco de dados
    
    def get(self, request, id):
        try:
            professional = Professionals.objects.get(id=id)
            serializer = ProfessionalSerializer(professional)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class ProfessionalUpdateView(APIView):
    # Atualiza os dados de um profissional
    
    permission_classes = [PermissionForProfessionals]
    
    def put(self, request, id):
        try:
            professional = Professionals.objects.get(id=id)
            serializer = ProfessionalSerializer(professional, data=request.data)
            user = User.objects.get(email=professional.email)
        
            user.username = request.data.get("name")
            user.password = make_password(request.data.get("password"))
            user.email = request.data.get("email")
            
            if serializer.is_valid():
                
                serializer.save()
                user.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe um prosissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class ProfessionalDeleteView(APIView):
    # Deleta um profissional do banco de dados
    
    permission_classes = [PermissionForProfessionals]
    
    def delete(self, request, id):
        try:
            professional = Professionals.objects.get(id=id)
            user = User.objects.get(email=professional.email)
            professional.delete()
            user.delete()
            
            return Response({"success": "Profissional deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um profissional com esse ID."}, status=status.HTTP_404_NOT_FOUND)
    