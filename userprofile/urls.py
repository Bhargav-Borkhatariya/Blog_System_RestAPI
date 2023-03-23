from django.urls import path
from userprofile.views import (
    UpdateUsernameAPIView,
    UserSoftDeleteAPIView,
)

urlpatterns = [
    # Update-Username API endpoint
    path("update-username/",
         UpdateUsernameAPIView.as_view(),
         name="updateusername"),

    # Soft-Delete-User API endpoint
    path("soft-delete-user/",
         UserSoftDeleteAPIView.as_view(),
         name="softdeleteuser"),
]
