from django.db import models

from patients.models import Patients
from professionals.models.professionals import Professionals
from professionals.models.specialties import Specialties


class Queries(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, null=False, related_name="queries")
    professional = models.ForeignKey(Professionals, on_delete=models.CASCADE, null=False, related_name="queries")
    date_hour = models.DateTimeField()
    status = models.CharField(max_length=100, choices=[('agendada', "Agendada"), ("realizada", 'Realizada'), ("cancelada", "Cancelada")], null=False)
    specialty = models.ForeignKey(Specialties, on_delete=models.RESTRICT, null=False, related_name="queries")
    observations = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
    
    
    def __str__(self):
        return f"{self.id}"
