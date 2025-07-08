from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductCardSerializer


class RealEstateProductFilterAPIView(APIView):
    """
    API to list and filter real estate products based on characteristics.
    Accepts filters as POST data.
    """
    CATEGORY_NAME = "Real Estate"

    def post(self, request, *args, **kwargs):
        queryset = Product.objects.filter(is_active=True, category__parent_category__name=self.CATEGORY_NAME)

        filters = request.data

        # Extract filter values
        transaction_type = filters.get("transaction_type")
        building_type = filters.get("building_type")
        room_count = filters.get("room_count")
        price_min = filters.get("price_min")
        price_max = filters.get("price_max")
        area_min = filters.get("area_min")
        area_max = filters.get("area_max")
        floor_min = filters.get("floor_min")
        floor_max = filters.get("floor_max")
        city = filters.get("city")
        renovation = filters.get("renovation")
        metro = filters.get("metro")
        landmark = filters.get("landmark")
        district = filters.get("district")
        additional_features = filters.get("additional_features", {})
        # "price_min": 50000
        # "price_max": 70000
        # "city": "Baku"
        # Apply filters
        if transaction_type:
            queryset = queryset.filter(characteristics__transaction_type=transaction_type)
        if building_type:
            queryset = queryset.filter(characteristics__building_type=building_type)
        if room_count:
            queryset = queryset.filter(characteristics__room_count=room_count)
        if price_min is not None:
            queryset = queryset.filter(characteristics__price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(characteristics__price__lte=price_max)
        if area_min is not None:
            queryset = queryset.filter(characteristics__area__gte=area_min)
        if area_max is not None:
            queryset = queryset.filter(characteristics__area__lte=area_max)
        if floor_min is not None:
            queryset = queryset.filter(characteristics__floor__gte=floor_min)
        if floor_max is not None:
            queryset = queryset.filter(characteristics__floor__lte=floor_max)
        if city:
            queryset = queryset.filter(characteristics__city__name=city)
        if renovation:
            queryset = queryset.filter(characteristics__renovation=renovation)
        if metro:
            queryset = queryset.filter(characteristics__metro__name=metro)
        if landmark:
            queryset = queryset.filter(characteristics__landmark__icontains=landmark)
        if district:
            queryset = queryset.filter(characteristics__district__name=district)

        # Apply additional features
        if isinstance(additional_features, dict):
            if additional_features.get("not_first_floor"):
                queryset = queryset.exclude(floor=1)
            if additional_features.get("not_last_floor"):
                queryset = queryset.exclude(floor__gte=floor_max)
            if additional_features.get("only_last_floor"):
                queryset = queryset.filter(floor=floor_max)
            if additional_features.get("has_mortgage"):
                queryset = queryset.filter(is_credit_available=True)
            if additional_features.get("has_document"):
                queryset = queryset.filter(has_document=True)
            if additional_features.get("has_barter"):
                queryset = queryset.filter(is_barter_available=True)

        # Serialize and return response
        serializer = ProductCardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# {
#     "price_min": 50000,
#     "price_max": 70000,
#     "city": "Baku",
#     "characteristics": {
#         "transaction_type": "sale",
#         "building_type": "apartment",
#         "room_count": 3,
#         "price_min": 50000,
#         "price_max": 200000,
#         "area_min": 50,
#         "area_max": 150,
#         "floor_min": 1,
#         "floor_max": 10,
#         "city": "Baku",
#         "renovation": "euro",
#         "is_mortgage_available": True,
#         "metro": "Nizami",
#         "landmark": "Park",
#         "district": "Yasamal",
#         "additional_features": {
#             "balcony": False,
#             "parking": False,
#             "elevator": False
#             }
#         }
# }