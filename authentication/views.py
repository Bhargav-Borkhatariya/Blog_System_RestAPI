from authentication.models import ActivationOTP
from authentication.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
)
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
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

            # Send email with OTP to the user
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


class VerifyActivationOtpView(APIView):
    """
    API View for verifying user OTP during account activation.
    """

    def post(self, request):
        """
        Verifies the OTP provided by the user for account activation.

        Parameters:
        request (HttpRequest): The HTTP request object containing the OTP.

        Returns:
        response (HttpResponse): A JSON response containing the status of
                OTP verification and a new auth token if verification is successful.
        """
        otp = request.data.get("otp")

        # Check if OTP is present in request data, if not then return an error response
        if not otp:
            return Response({
                "status": False,
                "message": "OTP is required field.",
                "data": None,
            }, status=HTTP_400_BAD_REQUEST)

        # Fetch user by OTP
        try:
            user_activation_otp = ActivationOTP.objects.get(otp=otp)
        except ObjectDoesNotExist:
            # If no user activation entry with the provided OTP is found, return an error response
            return Response({
                "status": False,
                "message": "OTP Verification failed",
                "data": None,
            }, status=HTTP_401_UNAUTHORIZED)

        # Get the user associated with the user activation entry
        user = user_activation_otp.user

        # Delete the old auth token
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()

        # Generate a new auth token for the user
        token = Token.objects.create(user=user)

        # Update the user activation status to True
        user.is_active = True
        user.save()

        # Return success response with the new auth token and user activation status update
        return Response({
            "status": True,
            "message": "OTP is Verified Successfully.",
            "data": {"token": token.key},
        }, status=HTTP_200_OK)
