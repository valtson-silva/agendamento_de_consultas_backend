from django.db import models
from patients.models import Patients
from professionals.models import Professionals
from professionals.models import Specialty

class Queries(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, null=False)
    professional = models.ForeignKey(Professionals, on_delete=models.CASCADE, null=False)
    date_hour = models.DateTimeField()
    status = models.CharField(max_length=100, choices=[('agendada', "Agendada"), ("realizada", 'Realizada'), ("cancelada", "Cancelada")], null=False)
    specialty = models.ForeignKey(Specialty, on_delete=models.RESTRICT, null=False)
    observations = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
