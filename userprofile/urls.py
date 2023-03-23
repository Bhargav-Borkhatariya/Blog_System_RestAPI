from django.urls import path
from userprofile.views import (
    UpdateUsernameAPIView,
    UserSoftDeleteAPIView,
    LogoutAPIView,
    RecoverSoftDeleteAPIView,
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

    # Logout API endpoint
    path("logout/",
         LogoutAPIView.as_view(),
         name="logout"),

    # Recover-Soft-Deleted User API endpoint.
    path("recover-soft-deleted-user/",
         RecoverSoftDeleteAPIView.as_view(),
         name="recoversoftdeleteduser"),
]
