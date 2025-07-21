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
from products.serializers import ProductCardSerializer

__all__ = (
    'UserDetailAPIView',
    'UserUpdateAPIView',
    'ProductCardListByUserAPIView',
    'UserProductStatusListAPIView',
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


class ProductCardListByUserAPIView(APIView):
    """List active products of a given user (by user_id)."""
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List user's active products",
        operation_description="""
        Returns a list of active products for a given user by user_id.

        Only products with `is_active=True` are returned.
        You can filter products by category using the `category_id` query parameter.
        """,
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Filter products by category ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: ProductCardSerializer(many=True)},
    )

    def get(self, request, user_id, *args, **kwargs):
        owner = get_object_or_404(User, id=user_id)
        products = Product.objects.filter(owner=owner, is_active=True)

        category_id = request.query_params.get('category_id')
        if category_id:
            products = products.filter(category_id=category_id)

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProductStatusListAPIView(APIView):
    """
    List current user's products with filters: status, activity, expired.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List current user's products with filters",
        operation_description="""
        You can filter your products using the following query parameters:

        - `status`: `approved`, `pending`, `expired`
        """,
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Product status (`approved` or `pending`)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Active status (`true` or `false`)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'expired',
                openapi.IN_QUERY,
                description="Filter expired products (`true`)",
                type=openapi.TYPE_BOOLEAN
            )
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

        # expired filter
        expired_products = request.query_params.get("expired")
        if expired_products:
            products = products.filter(is_active=False, status=Product.APPROVED)

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


