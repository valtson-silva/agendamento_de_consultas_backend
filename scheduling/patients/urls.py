from rest_framework.routers import DefaultRouter

from .views import PatientsViewSet


router = DefaultRouter()
router.register(r"api", PatientsViewSet, basename="patients")


urlpatterns = router.urls
