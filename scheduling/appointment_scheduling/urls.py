from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from authentication.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_auth_token),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('patients/', include('patients.urls')),
    path('professionals/', include('professionals.urls')),
    path('queries/', include('queries.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
