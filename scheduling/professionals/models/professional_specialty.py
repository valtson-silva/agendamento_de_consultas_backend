from django.db import models

from .professionals import Professionals
from .specialties import Specialties


class ProfessionalSpecialty(models.Model):
    specialty = models.ForeignKey(Specialties, on_delete=models.RESTRICT, null=False, related_name="professionals")
    professional = models.ForeignKey(Professionals, on_delete=models.RESTRICT, null=False, related_name="specialties")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Especialidade do Profissional"
        verbose_name_plural = "Especialidades dos Profissionais"
        constraints = [
            models.UniqueConstraint(fields=['specialty', 'professional'], name='unique_specialty_per_professional')
        ]
        