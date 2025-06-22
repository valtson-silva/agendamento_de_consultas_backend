from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models.professionals import Professionals
from .models.specialties import Specialties
from .models.professional_specialty import ProfessionalSpecialty
from patients.models import Patients


class ProfessionalSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Professionals
        fields =["id", "name", "email", "password", "address", "phone", "created_at", "updated_at"]
        
        
    def validate_email(self, value):
        if Patients.objects.filter(email=value).exists():
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


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialties
        fields = ["id", "name", "created_at", "updated_at"]
 
        
class ProfessionalSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalSpecialty
        fields = ["id", "specialty", "professional", "created_at", "updated_at"]
        