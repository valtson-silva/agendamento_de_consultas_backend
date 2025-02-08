from django.urls import path
from .views import (
    PatientCreateView, PatientDeleteView, PatientDetailView,
    PatientUpdateView, PatientsListView
)

# Endpoints
urlpatterns = [
    path("", PatientsListView.as_view(), name="patient_list"),
    path("<int:id>/", PatientDetailView.as_view(), name="patient_detail"),
    path("create/", PatientCreateView.as_view(), name="patient_create"),
    path("<int:id>/update/", PatientUpdateView.as_view(), name="patient_update"),
    path("<int:id>/delete/", PatientDeleteView.as_view(), name="patient_delete")
]