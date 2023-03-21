import configuration.utils.send_email as emailsender
from authentication.models import ActivationOTP
from authentication.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
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

            # Send email OTP to the user
            emailsender.send_activation_otp_email(user, otp)

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