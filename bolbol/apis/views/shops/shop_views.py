import json

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from shops.models import Shop, ShopActivity
from shops.serializers import (
    ShopSerializer,
    ShopRegistrationRequestSerializer,
    ShopActivitySerializer,
    ShopUpdateSerializer
)
from utils.constants import TimeIntervals

__all__ = (
    "ShopListAPIView",
    "ShopActivityListAPIView",
    "ShopRegistrationRequestAPIView",
    "ShopUpdateAPIView"
)


@method_decorator(cache_page(TimeIntervals.ONE_MONTH_IN_SEC), name="dispatch")
class ShopActivityListAPIView(APIView):
    http_method_names = ["get"]

    def get(self, request):
        shop_activities = ShopActivity.objects.filter(is_active=True)
        serializer = ShopActivitySerializer(shop_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopRegistrationRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        serializer = ShopRegistrationRequestSerializer(data=request.data)
        user = request.user
        shop_owner_full_name = request.data.get("shop_owner_full_name", "")
        user.full_name = shop_owner_full_name
        user.save(update_fields=["full_name"])

        if serializer.is_valid():
            shop_registration_request = serializer.save(shop_owner=user)
            return Response(
                ShopRegistrationRequestSerializer(shop_registration_request).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopListAPIView(APIView):
    """Retrieve all shops."""
    http_method_names = ["get"]
    permission_classes = [AllowAny]

    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            owner_data = json.loads(request.data.get("owner") or "{}")
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format for owner data"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        for field in ["full_name", "email"]:
            if field in owner_data:
                setattr(user, field, owner_data[field])
        user.save()

        # from shops.models import ShopActivity
        # shop_activites = [
        #     ShopActivity.objects.get(id=int(activity_id))
        #     for activity_id in request.data.get("activities").strip("[").strip("]").split(", ")
        # ]
        # shop = user.shop
        # shop.activities.set(shop_activites)
        # print(shop.activities.all())
        activities_str = request.data.get("activities", "").strip()

        if activities_str:
            try:
                activities_list = json.loads(activities_str) if activities_str.startswith("[") else list(map(int, activities_str.split(",")))
                if not isinstance(activities_list, list):
                    raise ValueError
            except (json.JSONDecodeError, ValueError, TypeError):
                return Response({"error": "activities must be a list of IDs"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch and set activities
            shop_activities = ShopActivity.objects.filter(id__in=activities_list)
            print(shop_activities)
            shop = user.shop
            shop.activities.set(shop_activities)

        # if activities_str:
        #     try:
        #         activities_list = json.loads(activities_str)  # Convert to list
        #         if not isinstance(activities_list, list):
        #             raise ValueError
        #         activities_list = [int(activity_id) for activity_id in activities_list]
        #     except (json.JSONDecodeError, ValueError, TypeError):
        #         return Response({"error": "activities must be a list of IDs"}, status=status.HTTP_400_BAD_REQUEST)

        #     # Fetch and set activities
        #     shop_activities = ShopActivity.objects.filter(id__in=activities_list)
        #     shop = user.shop
        #     shop.activities.set(shop_activities)
# API 
        serializer = ShopUpdateSerializer(instance=user.shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)