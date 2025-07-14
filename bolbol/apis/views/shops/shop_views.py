from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json

from products.models import Product
from shops.models import Shop, ShopWorkingHours, ShopContact, ShopActivity
from shops.serializers import (
    ShopSerializer,
    ShopDetailSerializer,
    ShopWorkingHoursSerializer,
    ShopContactSerializer,
    ShopRegistrationRequestSerializer,
    ShopActivitySerializer,
    ShopUpdateSerializer
)
from products.serializers import ProductCardSerializer
from utils.constants import TimeIntervals

__all__ = (
    "ShopListAPIView",
    "ShopDetailAPIView",
    "ProductCardListByShopAPIView",
    "ShopActivityListAPIView",
    "ShopRegistrationRequestAPIView",
    "CreateShopContactAPIView",
    "ShopUpdateAPIView",
    "ShopContactsAPIView",
    "CreateShopWorkingHoursAPIView",
    "ShopWorkingHoursAPIView"
)


@method_decorator(cache_page(TimeIntervals.ONE_MONTH_IN_SEC), name="dispatch")
class ShopActivityListAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List shop activities",
        operation_description="Returns a list of all active shop activities."
    )
    def get(self, request):
        shop_activities = ShopActivity.objects.filter(is_active=True)
        serializer = ShopActivitySerializer(shop_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopRegistrationRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    @swagger_auto_schema(
        request_body=ShopRegistrationRequestSerializer,
        operation_summary="Submit a shop registration request",
        operation_description="Authenticated users can submit a shop registration request."
    )
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopListAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List all shops",
        operation_description="Returns a list of all registered shops."
    )
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopDetailAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_summary="Get shop details",
        operation_description="Returns detailed information about a shop given its ID."
    )
    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, id=shop_id)
        serializer = ShopDetailSerializer(shop)
        return Response(serializer.data)


class ProductCardListByShopAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    is_vip_param = openapi.Parameter('is_vip', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, required=False)
    is_premium_param = openapi.Parameter('is_premium', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, required=False)

    @swagger_auto_schema(
        manual_parameters=[is_vip_param, is_premium_param],
        operation_summary="List products by shop",
        operation_description="Returns products for a given shop ID. Supports filtering by is_vip and is_premium."
    )
    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, id=shop_id)
        products = Product.objects.filter(is_active=True, owner=shop.owner).only(
            "name", "city__name", "updated_at", "price",
            "is_delivery_available", "is_barter_available", "is_credit_available",
            "is_super_chance", "is_premium", "is_vip"
        )

        is_vip = request.query_params.get("is_vip")
        is_premium = request.query_params.get("is_premium")

        if is_vip is not None:
            products = products.filter(is_vip=is_vip.lower() == "true")

        if is_premium is not None:
            products = products.filter(is_premium=is_premium.lower() == "true")

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'owner': openapi.Schema(type=openapi.TYPE_STRING, description='JSON string with full_name and email'),
                'activities': openapi.Schema(type=openapi.TYPE_STRING, description='List of activity IDs as JSON string or comma-separated')
            },
            required=['owner']
        ),
        operation_summary="Update shop profile",
        operation_description="Allows shop owner to update personal info and assigned activities."
    )
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

        activities_str = request.data.get("activities", "").strip()

        if activities_str:
            try:
                activities_list = json.loads(activities_str) if activities_str.startswith("[") else list(map(int, activities_str.split(",")))
                if not isinstance(activities_list, list):
                    raise ValueError
            except (json.JSONDecodeError, ValueError, TypeError):
                return Response({"error": "activities must be a list of IDs"}, status=status.HTTP_400_BAD_REQUEST)

            shop_activities = ShopActivity.objects.filter(id__in=activities_list)
            shop = user.shop
            shop.activities.set(shop_activities)

        serializer = ShopUpdateSerializer(instance=user.shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateShopContactAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=ShopContactSerializer,
        operation_summary="Create shop contact",
        operation_description="Authenticated shop owner can add a new contact to their shop."
    )
    def post(self, request):
        shop = Shop.objects.filter(owner=request.user).first()
        if not shop:
            return Response({"detail": "You must create a shop first."}, status=400)
        serializer = ShopContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopContactsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    @swagger_auto_schema(
        request_body=ShopContactSerializer,
        operation_summary="Update shop contact",
        operation_description="Update contact information by contact ID."
    )
    def patch(self, request, contact_id):
        contact = get_object_or_404(ShopContact, id=contact_id)
        serializer = ShopContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete shop contact",
        operation_description="Delete a shop contact by contact ID."
    )
    def delete(self, request, contact_id):
        contact = get_object_or_404(ShopContact, id=contact_id)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateShopWorkingHoursAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=ShopWorkingHoursSerializer,
        operation_summary="Create shop working hours",
        operation_description="Authenticated shop owner can create working hours."
    )
    def post(self, request):
        shop = Shop.objects.filter(owner=request.user).first()
        if not shop:
            return Response({"detail": "You must create a shop first."}, status=400)
        serializer = ShopWorkingHoursSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopWorkingHoursAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    @swagger_auto_schema(
        request_body=ShopWorkingHoursSerializer,
        operation_summary="Update working hours",
        operation_description="Update a shop's working hours by ID."
    )
    def patch(self, request, working_hour_id):
        working_hour = get_object_or_404(ShopWorkingHours, id=working_hour_id)
        serializer = ShopWorkingHoursSerializer(working_hour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete working hours",
        operation_description="Delete a shop's working hours by ID."
    )
    def delete(self, request, working_hour_id):
        working_hour = get_object_or_404(ShopWorkingHours, id=working_hour_id)
        working_hour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
