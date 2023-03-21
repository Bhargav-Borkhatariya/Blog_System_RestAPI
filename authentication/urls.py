from django.urls import path
from authentication.views import (
    RegistrationAPIView,
    VerifyActivationOtpView,
    SendOtpAcivationAPIView,
)

urlpatterns = [
    # Registration API endpoint
    path("register/",
         RegistrationAPIView.as_view(),
         name="register"),

    # User Verify OTP for forget pass API endpoint
    path("verify-activationotp/",
         VerifyActivationOtpView.as_view(),
         name="verify-activationotp"), 

    # Activate-Account API endpoint
    path("sendotp-activation/",
         SendOtpAcivationAPIView.as_view(),
         name="sendotp-activation"),
]
