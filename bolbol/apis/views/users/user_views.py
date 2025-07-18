from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, UserUpdateSerializer
from products.models import Product
from products.serializers import ProductCardSerializer, ProductDetailSerializer

__all__ = (
    'UserDetailAPIView',
    'UserUpdateAPIView',
    #'ProductCardListByUserAPIView',
    'ProductDetailByUserAPIView',
    'ProductPendingListByUserAPIView',
    'ProductApprovedListByUserAPIView',
    'ProductsExpireAtListByUserAPIView',
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

    
class ProductApprovedListByUserAPIView(APIView):
    """
    List current user's approved products.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List current user's approved products",
        manual_parameters=[
            openapi.Parameter(
                'is_vip',
                openapi.IN_QUERY,
                description="Filter by VIP status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_premium',
                openapi.IN_QUERY,
                description="Filter by Premium status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: ProductCardSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(
            owner=request.user,
            status=Product.APPROVED
        ).only(
            "name", "city__name", "updated_at", "created_at", "price",
            "is_delivery_available", "is_barter_available", "is_credit_available",
            "is_super_chance", "is_premium", "is_vip", "slug"
        )

        is_vip = request.query_params.get("is_vip")
        is_premium = request.query_params.get("is_premium")

        if is_vip is not None:
            products = products.filter(is_vip=is_vip.lower() == "true")

        if is_premium is not None:
            products = products.filter(is_premium=is_premium.lower() == "true")

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductPendingListByUserAPIView(APIView):
    """
    List current user's pending products.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List current user's pending products",
        manual_parameters=[
            openapi.Parameter(
                'is_vip',
                openapi.IN_QUERY,
                description="Filter by VIP status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_premium',
                openapi.IN_QUERY,
                description="Filter by Premium status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: ProductCardSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(
            owner=request.user,
            status=Product.PENDING
        ).only(
            "name", "city__name", "updated_at", "created_at", "price",
            "is_delivery_available", "is_barter_available", "is_credit_available",
            "is_super_chance", "is_premium", "is_vip", "slug"
        )

        is_vip = request.query_params.get("is_vip")
        is_premium = request.query_params.get("is_premium")

        if is_vip is not None:
            products = products.filter(is_vip=is_vip.lower() == "true")

        if is_premium is not None:
            products = products.filter(is_premium=is_premium.lower() == "true")

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsExpireAtListByUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    @swagger_auto_schema(
        operation_summary="List expired (inactive) approved products by user",
        operation_description="""
        Bu API istifadəçinin **təsdiqlənmiş lakin deaktiv (is_active=False)** məhsullarını qaytarır. 
        `is_vip` və `is_premium` query parametrləri ilə filtr edilə bilər.
        """,
        manual_parameters=[
            openapi.Parameter(
                'is_vip',
                openapi.IN_QUERY,
                description="VIP məhsulları göstər (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_premium',
                openapi.IN_QUERY,
                description="Premium məhsulları göstər (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: ProductCardSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(
            owner=request.user,
            status=Product.APPROVED,
            is_active=False
        ).only(
            "name", "city__name", "updated_at", "created_at", "price",
            "is_delivery_available", "is_barter_available", "is_credit_available",
            "is_super_chance", "is_premium", "is_vip", "slug"
        )
        is_vip = request.query_params.get("is_vip")
        is_premium = request.query_params.get("is_premium")
        
        if is_vip is not None:
            products = products.filter(is_vip=is_vip.lower() == "true")

        if is_premium is not None:
            products = products.filter(is_premium=is_premium.lower() == "true")
        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        