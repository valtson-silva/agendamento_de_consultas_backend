from django.urls import path
from .views import (
    QueriesListView, QueryCreateView, QueryDeleteView, QuerySpecialtyListView,
    QueryDetailView, QueryPatientListView, QueryProfessionalListView, QueryUpdateView
)

# Endpoints
urlpatterns = [
    path("", QueriesListView.as_view(), name="queries_list"),
    path("<int:id>/", QueryDetailView.as_view(), name="query_detail"),
    path("create/", QueryCreateView.as_view(), name="query_create"),
    path("<int:id>/update/", QueryUpdateView.as_view(), name="query_update"),
    path("<int:id>/delete/", QueryDeleteView.as_view(), name="query_delete"),
    path("<int:professional_id>/professional/", QueryProfessionalListView.as_view(), name="queries_professional_list"),
    path("<int:patient_id>/patient/", QueryPatientListView.as_view(), name="queries_patient_list"),
    path("<int:specialty_id>/specialty/", QuerySpecialtyListView.as_view(), name="queries_specialty_list")
]