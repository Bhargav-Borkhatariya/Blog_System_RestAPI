from django.contrib import admin
from authentication.models import ForgetPasswordOtp, ActivationOTP


# Register your models here.
admin.site.register((ForgetPasswordOtp, ActivationOTP))
