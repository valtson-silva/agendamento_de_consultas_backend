from django.contrib import admin

from .models.professionals import Professionals
from .models.specialties import Specialties
from .models.professional_specialty import ProfessionalSpecialty


admin.site.register(Professionals)
admin.site.register(Specialties)
admin.site.register(ProfessionalSpecialty)
