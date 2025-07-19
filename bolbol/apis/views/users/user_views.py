from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_datetime

from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, UserUpdateSerializer
from products.models import Product
from products.serializers import ProductCardSerializer, ProductDetailSerializer

__all__ = (
    'UserDetailAPIView',
    'UserUpdateAPIView',
    #'ProductCardListByUserAPIView',
    'ProductDetailByUserAPIView',
    'ProductListByUserAPIView',
)

User = get_user_model()

class UserDetailAPIView(APIView):
    """Retrieve user details by ID."""
    http_method_names = ["get"]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
        200: UserSerializer(),
        404: openapi.Response("User not found", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)}
        ))}       
    )

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User with the specified ID was not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Update current user",
        request_body=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer(),
            400: openapi.Response("Bad request", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(type=openapi.TYPE_STRING)
            ))}
    )

    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailByUserAPIView(APIView):
    """Retrieve user's active product detail."""
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    @swagger_auto_schema(
        operation_summary="Retrieve current user's product detail",
        manual_parameters=[
            openapi.Parameter(
                'product_slug',
                openapi.IN_PATH,
                description="Slug that starts with product ID (e.g. 42-some-product-name)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: ProductDetailSerializer()}
    )

    def get(self, request, product_slug, *args, **kwargs):
        product_pk = product_slug.split("-", 1)[0]
        product = get_object_or_404(Product, pk=product_pk, owner=request.user)

        product.views_count = F("views_count") + 1
        product.save()
        product.refresh_from_db()

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListByUserAPIView(APIView):
    """
    List current user's products with filters: status, activity, VIP, Premium, Expire Date.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List current user's products with filters",
        operation_description="""
        Aşağıdakı query parametrlərlə məhsullarınızı filtrləyə bilərsiniz:
        
        - `status`: `approved` və ya `pending`
        - `is_active`: `true` və ya `false`
        - `is_vip`: `true` və ya `false`
        - `is_premium`: `true` və ya `false`
        - `expire_at`: `YYYY-MM-DDTHH:MM:SSZ` formatında vaxt (məsələn, 2025-07-20T00:00:00Z)
        """,
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Məhsul statusu (`approved` və ya `pending`)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Aktivlik statusu (`true` və ya `false`)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_vip',
                openapi.IN_QUERY,
                description="VIP məhsulları göstər",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_premium',
                openapi.IN_QUERY,
                description="Premium məhsulları göstər",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'expires_at',
                openapi.IN_QUERY,
                description="Son istifadə tarixi (məs: 2025-07-20T00:00:00Z)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME
            ),
        ],
        responses={200: ProductCardSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(owner=request.user)

        # Status filter
        status_param = request.query_params.get("status")
        if status_param:
            if status_param.lower() == "approved":
                products = products.filter(status=Product.APPROVED)
            elif status_param.lower() == "pending":
                products = products.filter(status=Product.PENDING)

        # is_active filter
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            products = products.filter(is_active=is_active.lower() == "true")

        # is_vip filter
        is_vip = request.query_params.get("is_vip")
        if is_vip is not None:
            products = products.filter(is_vip=is_vip.lower() == "true")

        # is_premium filter
        is_premium = request.query_params.get("is_premium")
        if is_premium is not None:
            products = products.filter(is_premium=is_premium.lower() == "true")

        # expire_at filter
        expires_at_param = request.query_params.get("expires_at")
        if expires_at_param:
            parsed_expires_at = parse_datetime(expires_at_param)
            if parsed_expires_at:
                products = products.filter(expires_at__lte=parsed_expires_at)

        products = products.only(
            "name", "city__name", "updated_at", "created_at", "price",
            "is_delivery_available", "is_barter_available", "is_credit_available",
            "is_super_chance", "is_premium", "is_vip", "slug", "expires_at"
        )

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

