from django.db import models

class Specialties(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    