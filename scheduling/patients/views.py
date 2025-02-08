from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patients
from .serializers import PatientsSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class PatientCreateView(APIView):
    # Salva um paciente no banco de dados
    
    def post(self, request):
        # Serializa os dados recebidos no corpo da requisição
        serializer = PatientsSerializer(data=request.data)
        
        # Verifica se é válido
        if serializer.is_valid():
            # Salva o paciente no banco de dados
            serializer.save()
            
            # Cria o usuário com a senha criptografada
            User.objects.create_user(
                username=request.data["name"],
                password=request.data["password"],
                email=request.data["email"]
            )
            
            # Retorna o paciente salvo e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            
            # Retorna error e o status 400
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class PatientsListView(APIView):
    # Mostra todos os pacientes salvos no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtém todos os pacientes
        patients = Patients.objects.all()
        # Serializa os pacientes
        serializer = PatientsSerializer(patients, many=True)
        # Retorna todos os pacientes e o status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PatientDetailView(APIView):
    # Mostra os detalhes de um paciente que está no banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            # Tenta obter o paciente
            patient = Patients.objects.get(id=id)
            # Serializa o paciente
            serializer = PatientsSerializer(patient)
            # Retorna o paciente
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            # Retorna error e o status 404
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class PatientUpdateView(APIView):
    # Atualiza os dados de um paciente
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            # Tenta obter o paciente
            patient = Patients.objects.get(id=id)
            # Serializa os dados recebidos no corpo da requisição
            serializer = PatientsSerializer(patient, data=request.data)
            
            # Obtém o usuário pelo email 
            user = User.objects.get(email=patient.email)
            # Faz as alterações no usuário
            user.username = request.data.get("name")
            user.email = request.data.get("email")
            user.password = make_password(request.data.get("password"))
            
            # Verifica se os dados são válidos
            if serializer.is_valid():
                # Salva as alterações no banco de dados
                serializer.save()
                user.save()
                
                # Retorna os dados atualizados do paciente e o status 200
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                
                # Retorna error e o staus 400
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            
            # Retorna error e o status 404
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class PatientDeleteView(APIView):
    # Deleta um paciente do banco de dados
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            # Tenta obter o paciente 
            patient = Patients.objects.get(id=id)
            # Tenta obter o usuário
            user = User.objects.get(email=patient.email)
            # Deleta o paciente do banco de dados
            patient.delete()
            # Deleta o usuário do banco de dados
            user.delete()
            
            # Retorna sucesso e o status 200
            return Response({"success": "Paciente deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            
            # Retorna error e o status 404
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
            