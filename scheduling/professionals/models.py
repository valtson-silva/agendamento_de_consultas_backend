from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

class Professionals(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    
    
class ProfessionalSpecialty(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.RESTRICT, null=False)
    professional = models.ForeignKey(Professionals, on_delete=models.RESTRICT, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    