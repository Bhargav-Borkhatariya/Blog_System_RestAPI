from django.urls import path
from userprofile.views import (
    UpdateUsernameAPIView,
)

urlpatterns = [
    # Update-Username API endpoint
    path("update-username/",
         UpdateUsernameAPIView.as_view(),
         name="updateusername"),
]
