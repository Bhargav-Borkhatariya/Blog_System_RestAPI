from django.urls import path
from authentication.views import (
    RegistrationAPIView,
    VerifyActivationOtpView,
    SendOtpAcivationAPIView,
    EmailLoginAPIView,
    SendForgetPasswordOtpAPIView,
    VerifyforgetPassOtpView,
    UpdatePasswordAPIView,
)

urlpatterns = [
    # Registration API endpoint
    path("register/",
         RegistrationAPIView.as_view(),
         name="register"),

    # User Verify OTP for Activation API endpoint
    path("verify-activationotp/",
         VerifyActivationOtpView.as_view(),
         name="verify-activationotp"),

    # Activate-Account API endpoint
    path("sendotp-activation/",
         SendOtpAcivationAPIView.as_view(),
         name="sendotp-activation"),

    # Email Login API endpoint
    path("email-login/",
         EmailLoginAPIView.as_view(),
         name="email-login"),

    # Forget Password API endpoint
    path("sendotp-forget/",
         SendForgetPasswordOtpAPIView.as_view(),
         name="sendotp-forget"),

    # User Verify OTP for forget pass API endpoint
    path("verify-forgetotp/",
         VerifyforgetPassOtpView.as_view(),
         name="verify-forgetotp"),

    # Update Password API endpoint
    path("update-password/",
         UpdatePasswordAPIView.as_view(),
         name="forget-password"),

]
