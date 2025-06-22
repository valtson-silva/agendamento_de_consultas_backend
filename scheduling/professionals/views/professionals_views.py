from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from professionals.models.professionals import Professionals
from professionals.serializers import ProfessionalSerializer
from professionals.services.professionals_service import create_professionals_with_user, delete_profissional_with_user


class PermissionForProfessionals(BasePermission):
    """Criação de uma permissão customizada"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.has_perm("professionals.permission_for_professionals"):
            return True
        
        return False

class ProfessionalsViewSet(ModelViewSet):
    """CRUD dos profissionais"""
    
    queryset = Professionals.objects.all()
    serializer_class = ProfessionalSerializer
    
    
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            return [PermissionForProfessionals()]
        return [IsAuthenticated()]
    
    
    def create(self, request, *args, **kwargs):
        try:
            professional = create_professionals_with_user(request.data)
        except ValidationError as e:
            return Response({"success": False, "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(professional, status=status.HTTP_201_CREATED)
    
    
    def destroy(self, request, *args, **kwargs):
        try:
            professional_id = kwargs.get("pk")
            message = delete_profissional_with_user(professional_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": True, "message": message}, status=status.HTTP_204_NO_CONTENT)   
    
    def list(self, request, *args, **kwargs):
        cache_key = "professionals_list"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def retrieve(self, request, *args, **kwargs):
        professional_id = kwargs.get("pk")
        cache_key = f"professional_detail_{professional_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("pofessionals_list")
    
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete("professionals_list")    
        cache.delete(f"professional_detail_{instance.id}")
        
    
    def perform_destroy(self, instance):
        cache.delete("professional_list")
        cache.delete(f"professional_detail_{instance.id}")
        instance.delete()    
    