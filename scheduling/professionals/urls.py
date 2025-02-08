from django.urls import path
from .views_professionals import (
    ProfessionalCreateView, ProfessionalDeleteView, ProfessionalDetailView,
    ProfessionalListView, ProfessionalUpdateView
)
from .view_specialty_professional import (
    ProfessionalSpecialtyCreateView, ProfessionalSpecialtyDeleteView, 
    ProfessionalSpecialtyListView, ProfessionalSpecialtyUpdateView, SpecialtyProfessionalListView
)
from .view_specialty import (
    SpecialtyCreateView, SpecialtyDeleteView, SpecialtyDetailView,
    SpecialtyListView, SpecialtyUpdateView
)

# Endpoints
urlpatterns = [
    path("", ProfessionalListView.as_view(), name="professionals_list"),
    path("<int:id>/", ProfessionalDetailView.as_view(), name="professional_detail"),
    path("create/", ProfessionalCreateView.as_view(), name="professional_create"),
    path("<int:id>/update/", ProfessionalUpdateView.as_view(), name="professional_update"),
    path("<int:id>/delete/", ProfessionalDeleteView.as_view(), name="professional_delete"),
    path("specialty/create/", SpecialtyCreateView.as_view(), name="specialty_create"),
    path("specialty/", SpecialtyListView.as_view(), name="specialty_list"),
    path("specialty/<int:id>/update/", SpecialtyUpdateView.as_view(), name="specialty_update"),
    path("specialty/<int:id>/", SpecialtyDetailView.as_view(), name="specialty_detail"),
    path("specialty/<int:id>/delete/", SpecialtyDeleteView.as_view(), name="specialty_delete"),
    path("<int:professional_id>/specialty/list/", ProfessionalSpecialtyListView.as_view(), name="professional_specialty_list"),
    path("specialty/<int:specialty_id>/list/", SpecialtyProfessionalListView.as_view(), name="specialty_professional_list"),
    path("professional_specialty/create/", ProfessionalSpecialtyCreateView.as_view(), name="professional_specialty_create"),
    path("professional_specialty/<int:id>/update/", ProfessionalSpecialtyUpdateView.as_view(), name="professional_specialty_update"),
    path("professional_specialty/<int:id>/delete/", ProfessionalSpecialtyDeleteView.as_view(), name="professional_specialty_delete")
]