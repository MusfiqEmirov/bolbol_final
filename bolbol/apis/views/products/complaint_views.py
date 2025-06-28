import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction

from products.models import ComplaintCategory
from products.serializers import ComplaintCreateSerializer, ComplaintCategorySerializer
from utils.constants import TimeIntervals

__all__ = (
    "ComplaintCreateAPIView",
    "ComplaintCategoryAPIView"
)

logger = logging.getLogger(__name__)

@method_decorator(cache_page(TimeIntervals.ONE_MONTH_IN_SEC), name="dispatch")
class ComplaintCategoryAPIView(APIView):
    """Endpoint to list categories with essential fields, cached for 1 month."""

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        categories = ComplaintCategory.objects.all().order_by("name")
        serializer = ComplaintCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComplaintCreateAPIView(APIView):
    """Endpoint to create complaints, requires authentication and rate limiting."""

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = ComplaintCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save(complainant=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Complaint creation failed: {e}")
                return Response(
                    {"detail": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        logger.warning(f"Complaint validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)