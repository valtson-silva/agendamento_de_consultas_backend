from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from professionals.serializers import SpecialtySerializer
from professionals.models.specialties import Specialties
from .professionals_views import PermissionForProfessionals


class SpecialtiesViewSet(ModelViewSet):
    """CRUD das especialidades"""
    
    queryset = Specialties.objects.all()
    serializer_class = SpecialtySerializer
    
    
    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            return [IsAuthenticated()]
        return [PermissionForProfessionals()]
    
    
    def list(self, request, *args, **kwargs):
        cache_key = "specialties_list"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def retrieve(self, request, *args, **kwargs):
        specialty_id = kwargs.get("pk")
        cache_key = f"spacialty_detail_{specialty_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("specialties_list")
        
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete("specialties_list")
        cache.delete(f"specialty_detail_{instance.id}")
        
    
    def perform_destroy(self, instance):
        cache.delete("specialties_list")
        cache.delete(f"specialty_detail_{instance.id}")
        instance.delete()
        