from rest_framework import serializers
from .models import Patients
from professionals.models import Professionals
from django.contrib.auth.hashers import make_password

class PatientsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        # Define o modelo
        model = Patients
        # Define os campos
        fields = ["id", "name", "email", "password", "address", "phone", "created_at", "date_update"]
        
        
    def validate_email(self, value):
        # Verifica se o email já está em uso
        if Professionals.objects.filter(email=value).exists():
            raise serializers.ValidationError("Esse email já está em uso!")
        return value
    
    def validate_password(self, value):
        # Criptografa a senha
        return make_password(value)


    def save(self, **kwargs):
        return super().save(**kwargs)
        
 