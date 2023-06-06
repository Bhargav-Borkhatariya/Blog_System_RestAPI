from django.contrib import admin
from authentication.models import (
    ForgetPasswordOtp,
    ActivationOTP,
    SoftDeletedUser
    )


@admin.register(ForgetPasswordOtp)
class ForgetPasswordOtpAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "created_at")
    list_filter = ("created_at",)


@admin.register(ActivationOTP)
class ActivationOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "created_at")
    list_filter = ("created_at",)


@admin.register(SoftDeletedUser)
class SoftDeletedUserAdmin(admin.ModelAdmin):
    list_display = ("user", "deleted_at")
    list_filter = ("deleted_time",)
