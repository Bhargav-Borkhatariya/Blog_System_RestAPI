from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_activation_otp_email(user, otp):
    email_subject = f"Activation OTP for {user}"
    email_body = render_to_string("activation.txt", {"user": user, "otp": otp})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()


def send_forget_password_otp_email(user, otp):
    email_subject = f"Forget Password OTP for {user}"
    email_body = render_to_string("forget_pass.txt", {"user": user, "otp": otp})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()
