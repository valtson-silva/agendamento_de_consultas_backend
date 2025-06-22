from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Patients
from professionals.models.professionals import Professionals


class PatientsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Patients
        fields = ["id", "name", "email", "password", "address", "phone", "created_at", "date_update"]
        
        
    def validate_email(self, value):
        if Professionals.objects.filter(email=value).exists():
            raise serializers.ValidationError("Esse email já está em uso!")
        return value
    
    def validate_name(self, value):
        if Professionals.objects.filter(name=value).exists() or Patients.objects.filter(name=value).exists():
            raise serializers.ValidationError("Esse name já está em uso!")
        return value
    
    def validate_password(self, value):
        return make_password(value)


    def save(self, **kwargs):
        return super().save(**kwargs)
        