from django.urls import path

from professionals.views.professional_specialty_views import (
    MyCreateUpdateDeleteView, ProfessionalSpecialtyListView, SpecialtyProfessionalListView
)


urlpatterns = [
    path("api/", MyCreateUpdateDeleteView.as_view(), name="professional-specialty-create"),
    path("api/<int:pk>/", MyCreateUpdateDeleteView.as_view(), name="professional-specialty-detail"),
    path("api/professional/<int:professional_id>/", ProfessionalSpecialtyListView.as_view(), name="professional-specialties-list"),
    path("api/specialty/<int:specialty_id>/", SpecialtyProfessionalListView.as_view(), name="specialty-professionals-list"),
]
