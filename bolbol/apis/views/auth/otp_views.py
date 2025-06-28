from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from services.notifications import send_sms_alert

from utils.helpers import generate_otp_code, normalize_phone_number
from utils.validators import validate_phone_number
from utils.configs import OTPConfig
from utils.constants import TimeIntervals

from django.contrib.auth import get_user_model

__all__ = (
    "SendOTPAPIView",
    "VerifyOTPAPIView"
)


User = get_user_model()

class SendOTPAPIView(APIView):
    """
    Send OTP to a given phone number.
    """

    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_summary="Send OTP Code",
        operation_description="Sends an OTP to the provided phone number after validation and rate-limiting checks.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="User's phone number")
            },
            required=["phone_number"]
        ),
        responses={
            200: openapi.Response("OTP sent successfully!", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"message": openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: "Bad Request - Missing or Invalid Phone Number",
            429: "Too Many Requests - Rate limit exceeded"
        }
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
                {"error": "Phone number is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            phone_number = normalize_phone_number(phone_number=phone_number)
            validate_phone_number(phone_number)
        except ValidationError as e:
            return Response(
                {"error": str(e.message)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_key = f"otp_{phone_number}"
        otp_cooldown_key = f"otp_cooldown_{phone_number}"
        attempt_count_key = f"otp_attempts_{phone_number}"

        if cache.get(otp_cooldown_key):
            return Response(
                {"error": "Too many OTP requests. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        attempt_count = cache.get(attempt_count_key, 0)
        if attempt_count >= OTPConfig.OTP_ATTEMPT_LIMIT:
            return Response(
                {"error": "You have exceeded the maximum number of OTP attempts."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        otp_code = generate_otp_code()

        cache.set(otp_key, otp_code, timeout=OTPConfig.OTP_EXPIRY)
        cache.set(otp_cooldown_key, True, timeout=OTPConfig.OTP_COOLDOWN)
        cache.set(attempt_count_key, attempt_count+1, timeout=TimeIntervals.ONE_DAY_IN_SEC)

        send_sms_alert(phone_number, f"Your OTP code is {otp_code}")
        # send_sms_alert.delay(phone_number, f"Your OTP code is {otp_code}")

        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    """
    Verify OTP and authenticate the user.
    """

    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_summary="Verify OTP Code",
        operation_description="Verifies the OTP for a given phone number and returns JWT tokens if successful.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="User's phone number"),
                "otp_code": openapi.Schema(type=openapi.TYPE_STRING, description="One-time password (OTP)")
            },
            required=["phone_number", "otp_code"]
        ),
        responses={
            200: openapi.Response("OTP verified successfully!", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
            400: "Bad Request - Invalid OTP or phone number",
            401: "Unauthorized - OTP expired or incorrect"
        }
    )
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = request.data.get("otp_code")

        if not phone_number or not otp_code:
            return Response(
                {"error": "Phone number and OTP code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            phone_number = normalize_phone_number(phone_number=phone_number)
            validate_phone_number(phone_number)
        except ValidationError as e:
            return Response(
                {"error": str(e.message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_key = f"otp_{phone_number}"
        stored_otp = cache.get(otp_key)

        if not stored_otp:
            return Response(
                {"error": "OTP has expired or is invalid. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(stored_otp) != str(otp_code):
            return Response(
                {"error": "Invalid OTP. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(phone_number=phone_number)

        attempt_count_key = f"otp_attempts_{phone_number}"
        cache.delete(attempt_count_key)
        cache.delete(otp_key)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "detail": "OTP verified successfully!",
            "user_id": user.pk,
            "access": access_token,
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)