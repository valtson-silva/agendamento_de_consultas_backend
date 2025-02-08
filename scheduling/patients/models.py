from django.db import models

class Patients(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    