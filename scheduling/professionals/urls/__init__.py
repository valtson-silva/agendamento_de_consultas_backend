from django.urls import path, include

from .professionals import urlpatterns as professionals_urls
from .specialties import urlpatterns as specialties_urls
from .pofessional_specialty import urlpatterns as professionals_specialty_urls


urlpatterns = [
    path("", include(professionals_urls)),
    path("specialties/", include(specialties_urls)),
    path("professional/specialty/", include(professionals_specialty_urls)),
]
