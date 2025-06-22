from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

from .serializers import QuerySerializer
from .models import Queries
from professionals.views.professionals_views import PermissionForProfessionals
from .queries_service import query_patient, query_professional, query_specialty


class QueriesViewSet(ModelViewSet):
    queryset = Queries.objects.all()
    serializer_class = QuerySerializer
    
    
    def get_permissions(self):
        if self.action == "list":
            return [PermissionForProfessionals()]
        return [IsAuthenticated()]
    
    
    def list(self, request, *args, **kwargs):
        cache_key = "queries_list"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def retrieve(self, request, *args, **kwargs):
        query_id = kwargs.get("pk")
        cache_key = f"query_detail_{query_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
    
    
    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("queries_list")
        
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete("queries_list")
        cache.delete(f"query_detail_{instance.id}")
        
    
    def perform_destroy(self, instance):
        cache.delete("queries_list")
        cache.delete(f"query_detail_{instance.id}")
        instance.delete()
        
        
class QueryProfessionalListView(APIView):
    """Mostra todas as consultas referentes a um profissional"""
    
    permission_classes = [PermissionForProfessionals]
    
    def get(self, request, professional_id):
        try:
            queries = query_professional(professional_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(queries, status=status.HTTP_200_OK)


class QueryPatientListView(APIView):
    """Mostra todas as consultas referentes a um paciente"""
    
    def get(self, request, patient_id):
        try:
            queries = query_patient(patient_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(queries, status=status.HTTP_200_OK)
        
        
class QuerySpecialtyListView(APIView):
    """Mostra todas as consultas referentes a uma especialidade"""
    
    permission_classes = [PermissionForProfessionals]
    
    def get(self, request, specialty_id):
        try:
            queries = query_specialty(specialty_id)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(queries, status=status.HTTP_200_OK)
            