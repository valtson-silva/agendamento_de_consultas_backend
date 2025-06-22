from django.db import models


class Professionals(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=150, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("permission_for_professionals", "Pode acessar informações gerais")
        ]

        ordering = ['name']
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        
        
    def __str__(self):
        return self.name
    