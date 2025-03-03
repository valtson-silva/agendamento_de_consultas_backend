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
        serializer = PatientsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            User.objects.create_user(
                username=request.data["name"],
                password=request.data["password"],
                email=request.data["email"]
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class PatientsListView(APIView):
    # Mostra todos os pacientes salvos no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        patients = Patients.objects.all()
        serializer = PatientsSerializer(patients, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PatientDetailView(APIView):
    # Mostra os detalhes de um paciente que está no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            patient = Patients.objects.get(id=id)
            serializer = PatientsSerializer(patient)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)

class PatientUpdateView(APIView):
    # Atualiza os dados de um paciente
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            patient = Patients.objects.get(id=id)
            serializer = PatientsSerializer(patient, data=request.data)
            user = User.objects.get(email=patient.email)
            # Faz as alterações no usuário
            user.username = request.data.get("name")
            user.email = request.data.get("email")
            user.password = make_password(request.data.get("password"))
            
            if serializer.is_valid():
                serializer.save()
                user.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados informados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        
class PatientDeleteView(APIView):
    # Deleta um paciente do banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            patient = Patients.objects.get(id=id)
            user = User.objects.get(email=patient.email)
            patient.delete()
            user.delete()
            
            return Response({"success": "Paciente deletado com sucesso."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe um paciente com esse ID."}, status=status.HTTP_404_NOT_FOUND)
        