from django.db import models
from django.contrib.auth.models import User


class ActivationOTP(models.Model):
    """
    Model representing an activation OTP for user account activation.

    Attributes:
        user (ForeignKey): A reference to the User for whom the activation OTP was generated.
        otp (CharField): The OTP code generated for user account activation.
        created_at (DateTimeField): The date and time when the activation OTP was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activation OTP {self.otp} for {self.user.email}"
