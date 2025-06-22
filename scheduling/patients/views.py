from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from professionals.views.professionals_views import PermissionForProfessionals
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from .models import Patients
from .serializers import PatientsSerializer
from .patients_service import create_patient_with_user, delete_patient_with_user


class PatientsViewSet(ModelViewSet):
    """CRUD dos pacientes"""
    
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer
    
    
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "list":
            return [PermissionForProfessionals()]
        return [IsAuthenticated()]
    
    
    def create(self, request, *args, **kwargs):
        try:
            patient = create_patient_with_user(request.data)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"success": False, "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(patient, status=status.HTTP_201_CREATED)
    
    
    def destroy(self, request, *args, **kwargs):
        try:
            patient_id = kwargs.get("pk")
            message = delete_patient_with_user(patient_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"success": True, "message": message}, status=status.HTTP_204_NO_CONTENT)
    
    
    def list(self, request, *args, **kwargs):
        cache_key = "patients_list"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get("pk")
        cache_key = f"patient_detail_{patient_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout= 60 * 5)
        return response
    
    
    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("patients_list")
        
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete("patients_list")
        cache.delete(f"patient_detail_{instance.id}")
        
    
    def perform_destroy(self, instance):
        cache.delete("patients_list")
        cache.delete(f"patient_detail_{instance.id}")
        instance.delete()
        