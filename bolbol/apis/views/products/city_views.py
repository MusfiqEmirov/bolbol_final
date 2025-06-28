from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import City
from products.serializers import CitySerializer
from utils.constants import TimeIntervals

__all__ = ("CityListAPIView",)


@method_decorator(cache_page(TimeIntervals.ONE_YEAR_IN_SEC), name="dispatch")
class CityListAPIView(APIView):
    """Endpoint to list all cities with caching."""
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        cities = City.objects.filter(is_active=True)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)