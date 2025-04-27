from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

# Endpoints
urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_auth_token),
    path("patients/", include("patients.urls")),
    path("professionals/", include("professionals.urls")),
    path("queries/", include("queries.urls")),
]
