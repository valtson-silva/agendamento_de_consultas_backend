from rest_framework.routers import DefaultRouter

from professionals.views.specialties_views import SpecialtiesViewSet


router = DefaultRouter()
router.register(r"api", SpecialtiesViewSet, basename="specialties")


urlpatterns = router.urls