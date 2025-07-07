from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductCardSerializer
from .filter_handler import filter_transport_characteristics

__all__ = ("TransportProductFilterAPIView",)


class TransportProductFilterAPIView(APIView):
    """
    API to list and filter transport-related products based on characteristics.
    Accepts filters as POST data.
    """
    CATEGORY_NAME = "Transport"

    def post(self, request, *args, **kwargs):
        queryset = Product.objects.filter(is_active=True, category__parent_category__name=self.CATEGORY_NAME)
        filters = request.data

        price_min = filters.get("price_min")
        price_max = filters.get("price_max")
        city = filters.get("city")
        is_credit_available = filters.get("is_credit_available")
        is_barter_available = filters.get("is_barter_available")

        is_vip = request.GET.get("is_vip")
        is_premium = request.GET.get("is_premium")

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        if city is not None:
            queryset = queryset.filter(city__name=city)
        if is_vip is not None:
            queryset = queryset.filter(is_vip=bool(is_vip))
        if is_premium is not None:
            queryset = queryset.filter(is_premium=bool(is_premium))
        if is_credit_available is not None:
            queryset = queryset.filter(is_credit_available=bool(is_credit_available))
        if is_barter_available is not None:
            queryset = queryset.filter(is_barter_available=bool(is_barter_available))

        characteristics_filter = filters.get("characteristics", {})
        if characteristics_filter:
            if not isinstance(characteristics_filter, dict):
                return Response({"error": "Characteristics must be a JSON object"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = filter_transport_characteristics(queryset, characteristics_filter)

        serializer = ProductCardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)