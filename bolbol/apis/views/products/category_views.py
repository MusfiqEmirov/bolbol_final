from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from products.models import Category, CategoryFilterField
from products.serializers import CategorySerializer
from utils.constants import TimeIntervals

__all__ = (
    "CategoryAPIView",
)


# @method_decorator(cache_page(TimeIntervals.ONE_MONTH_IN_SEC), name="dispatch")
class CategoryAPIView(APIView):
    """Endpoint to list only parent categories with their subcategories."""
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        parent_categories = Category.objects.filter(is_active=True, parent_category__isnull=True)
        serializer = CategorySerializer(parent_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)