from authentication.models import ActivationOTP
from authentication.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string


class RegistrationAPIView(APIView):
    """
    API View to register a new user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user account by accepting user details

        Parameters:
        request (Request): The incoming request object

        Returns:
        Response: JSON response containing the user's details and
                  the authentication token if successful.
                  Error response if request is invalid or
                  user with the same email already exists.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP and save to the database
            otp = get_random_string(length=6, allowed_chars="0123456789")
            ActivationOTP.objects.create(user=user, otp=otp)

            # Send email with the authtoken and OTP to the user
            email_subject = f"Activation OTP for the {user}"
            email_body = render_to_string(
                "activation.txt", {"user": user, "otp": otp}
            )
            email = EmailMessage(
                email_subject,
                email_body,
                to=[user.email],
            )
            email.send()

            return Response({
                "status": True,
                "message": "User created successfully",
                "data": None,
            }, status=HTTP_201_CREATED)
        else:
            return Response({
                "status": False,
                "errors": serializer.errors,
                "data": None
            }, status=HTTP_400_BAD_REQUEST)