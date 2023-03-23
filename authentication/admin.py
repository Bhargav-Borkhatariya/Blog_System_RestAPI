from django.contrib import admin
from authentication.models import ForgetPasswordOtp, ActivationOTP, User


# Register your models here.
admin.site.register((ForgetPasswordOtp, ActivationOTP, User))
