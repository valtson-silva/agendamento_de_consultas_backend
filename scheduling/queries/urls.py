from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuerySpecialtyListView, QueriesViewSet,
    QueryPatientListView, QueryProfessionalListView
)


router = DefaultRouter()
router.register(r"api", QueriesViewSet, basename="queries")


urlpatterns = [
    path("professional/<int:professional_id>/", QueryProfessionalListView.as_view(), name="queries-professional-list"),
    path("patient/<int:patient_id>/", QueryPatientListView.as_view(), name="queries-patient-list"),
    path("specialty/<int:specialty_id>/", QuerySpecialtyListView.as_view(), name="queries-specialty-list"),
    path("", include(router.urls))
]
