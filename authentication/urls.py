from django.urls import path
from authentication.views import (
    RegistrationAPIView,
)

urlpatterns = [
    # Registration API endpoint
    path("register/",
         RegistrationAPIView.as_view(),
         name="register"),
]
