from rest_framework.routers import DefaultRouter

from professionals.views.professionals_views import ProfessionalsViewSet


router = DefaultRouter()
router.register(r"api", ProfessionalsViewSet, basename="professionals")


urlpatterns = router.urls
