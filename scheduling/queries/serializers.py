from rest_framework import serializers
from .models import Queries

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        # Define o modelo
        model = Queries
        # Define os campos
        fields = ["id", "patient", "professional", "date_hour", "status", "specialty", "observations", "created_at", "date_update"]
        