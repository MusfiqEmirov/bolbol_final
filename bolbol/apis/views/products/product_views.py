import json
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from utils.helpers import convert_decimal_to_float
from utils.algorithms import _get_similar_products
from products.models import(
    Product, 
    ProductPhoto, 
    ReactivationRequest, 
    ProductUpdateRequest
    )
from products.serializers import(
    ProductCardSerializer, 
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer
    # ProductDeactivateSerializer
    )   


__all__ = (
    "ProductCardListAPIView",
    "ProductDetailAPIView",
    "ProductCreateAPIView",
    "ProductUpdateRequestAPIView",
    "SimilarProductListAPIView",
    "RequestProductReactivationAPIView",
    "BulkDeleteProductsAPIView",   
)


class BulkDeleteProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    @swagger_auto_schema(
        request_body=ProductDeleteSerializer,
        responses={200: "Products deleted successfully."}
    )
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

    @swagger_auto_schema(
        responses={200: ProductCardSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter("is_vip", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="VIP filter"),
            openapi.Parameter("is_premium", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Premium filter"),
        ]
    )
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

    @swagger_auto_schema(
        responses={200: ProductDetailSerializer()}
    )
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


class RequestProductReactivationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Request reactivation of an inactive product by slug.",
        responses={
            201: openapi.Response("Reactivation request sent successfully."),
            400: openapi.Response("Product already active or request already exists."),
            404: openapi.Response("Product not found."),
        }
    )
    def post(self, request, product_slug):
        product_pk = product_slug.split("-", 1)[0]
        try:
            product = Product.objects.get(pk=product_pk, owner=request.user)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)

        if product.is_active:
            return Response({"detail": "Product is already active."}, status=400)

        exists = ReactivationRequest.objects.filter(
            product=product,
            user=request.user,
            status=ReactivationRequest.PENDING
        ).exists()

        if exists:
            return Response({"detail": "You already have a pending reactivation request."}, status=400)

        ReactivationRequest.objects.create(product=product, user=request.user)
        return Response({"detail": "Reactivation request sent successfully."}, status=201)


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
    

class ProductUpdateRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=ProductUpdateSerializer,
        responses={
            202: openapi.Response("Update request submitted for moderation."),
            400: "Validation error or business logic error (e.g. pending request exists, product inactive or expired).",
            404: "Product not found."
        }
    )
    def post(self, request, product_slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=product_slug, owner=request.user)

        if ProductUpdateRequest.objects.filter(product=product, status=ProductUpdateRequest.PENDING).exists():
            return Response({"error": "An update request is already pending for this product."}, status=status.HTTP_400_BAD_REQUEST)

        if not product.is_active:
            return Response({"error": "This product is not active."}, status=status.HTTP_400_BAD_REQUEST)

        if product.expires_at and product.expires_at < timezone.now():
            return Response({"error": "Product has already expired."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            owner_data = json.loads(request.data.get("owner") or "{}")
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format for owner data"}, status=status.HTTP_400_BAD_REQUEST)

        temp_user_data = {}
        for field in ["full_name", "email"]:
            if field in owner_data:
                temp_user_data[field] = owner_data[field]

        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = convert_decimal_to_float(serializer.validated_data)

            photos = request.FILES.getlist("photos")
            photo_data = []
            for index, image in enumerate(photos):
                photo_data.append({
                    "name": image.name,
                    "size": image.size,
                    "content_type": image.content_type,
                })

            ProductUpdateRequest.objects.create(
                product=product,
                data=validated_data,
                user_data=temp_user_data,
                photo_meta=photo_data,
                status=ProductUpdateRequest.PENDING
            )

            return Response({"message": "Update request submitted for moderation."}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
