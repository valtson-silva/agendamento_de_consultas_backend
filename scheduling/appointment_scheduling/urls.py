from django.contrib import admin
from django.urls import path, include
from user.views import LogoutView, UserLogarView

# Endpoints
urlpatterns = [
    path('admin/', admin.site.urls),
    path("patients/", include("patients.urls")),
    path("professionals/", include("professionals.urls")),
    path("queries/", include("queries.urls")),
    path("login/", UserLogarView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
