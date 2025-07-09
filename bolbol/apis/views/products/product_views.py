import json

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.db.models import F
from django.db import transaction

from products.models import Product, ProductPhoto
from products.serializers import ProductCreateSerializer
from products.serializers.product_serializer import ProductDeleteSerializer

from products.models import Product
from products.serializers import (
    ProductCardSerializer, 
    ProductCreateSerializer,
    ProductDetailSerializer,
    # ProductDeactivateSerializer
)
from utils.algorithms import _get_similar_products

__all__ = (
    "ProductCardListAPIView",
    "ProductDetailAPIView",
    "ProductCreateAPIView",
    "SimilarProductListAPIView",
    "BulkDeleteProductsAPIView",
)


class BulkDeleteProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    def delete(self, request):
        serializer = ProductDeleteSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        try:
            with transaction.atomic():
                products_to_delete = Product.objects.filter(id__in=ids)
                deleted_count, _ = products_to_delete.delete()
        except Exception as e:
            return Response({"error": f"Deletion failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": f"{deleted_count} product(s) deleted successfully.",
            "deleted_ids": ids
        }, status=status.HTTP_200_OK)
    

class ProductCardListAPIView(APIView):
    """Endpoint to list products with essential fields."""
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=True).only(
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


class ProductDetailAPIView(APIView):
    """Endpoint to retrieve detailed product information."""
    http_method_names = ["get"]

    def get(self, request, product_slug, *args, **kwargs):
        product_pk = product_slug.split("-", 1)[0]
        product = get_object_or_404(Product, pk=product_pk, is_active=True)

        product.views_count = F("views_count") + 1
        product.save()
        product.refresh_from_db()

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarProductListAPIView(APIView):
    """Endpoint to retrieve similar products."""
    http_method_names = ["get"]

    def get(self, request, product_slug, *args, **kwargs):
        product_pk = product_slug.split("-", 1)[0]
        main_product = get_object_or_404(Product, pk=product_pk, is_active=True)
        similar_products = _get_similar_products(main_product)
        serializer = ProductCardSerializer(similar_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class ProductCreateAPIView(APIView):
#     """Endpoint to create a new product."""
#     http_method_names = ["post"]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = ProductCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class ProductCreateAPIView(APIView):
#     """
#     API View for creating a product along with multiple product photos.
#     """
#     permission_classes = [AllowAny]  # Or use IsAuthenticated if needed
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         owner_data_str = request.data.get("owner")

#         if owner_data_str:
#             try:
#                 owner_data = json.loads(owner_data_str)
#             except json.JSONDecodeError:
#                 return Response({"error": "Invalid JSON format for owner data"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             owner_data = {}

#         user = request.user

#         user.full_name = owner_data.get("owner_full_name", user.full_name)
#         user.email = owner_data.get("owner_email", user.email)
#         user.save()

#         serializer = ProductCreateSerializer(data=request.data)

#         if serializer.is_valid():
#             product = serializer.save(owner=request.user)

#             photos_data = request.FILES.getlist("photos")
#             for index, image in enumerate(photos_data):
#                 ProductPhoto.objects.create(
#                     product=product,
#                     image=image,
#                     order=index
#                 )

#             return Response({"id": product.id, "message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateAPIView(APIView):
    """
    API View for creating a product along with multiple product photos.
    """
    permission_classes = [IsAuthenticated]  # Ensure user is logged in
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            owner_data = json.loads(request.data.get("owner") or "{}")
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format for owner data"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        for field in ["full_name", "email"]:
            if field in owner_data:
                setattr(user, field, owner_data[field])
        user.save()

        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(owner=user)

            ProductPhoto.objects.bulk_create([
                ProductPhoto(product=product, image=image, order=index)
                for index, image in enumerate(request.FILES.getlist("photos"))
            ])

            return Response({"id": product.id, "message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)