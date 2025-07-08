from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from django.db.models import Q



from products.models import Product, ProductPhoto
from users.serializers import ProductOwnerMiniProfileSerializer, UserSerializer
from .comment_serializer import CommentSerializer
from .product_photo_serializer import ProductPhotoSerializer, ProductPhotoCreateSerializer


class ProductCardSerializer(serializers.ModelSerializer):
    """
    Serializer for listing products with essential fields.
    """
    city = serializers.CharField(source="city.name", read_only=True)
    absolute_url = serializers.CharField(source="get_absolute_url")
    preview_photo_url = serializers.CharField(source="get_preview_photo_url")

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "absolute_url",
            "preview_photo_url",
            "name",
            "city",
            "updated_at",
            "created_at",
            "price",

            "is_delivery_available",
            "is_barter_available",
            "is_credit_available",

            "is_super_chance",
            "is_premium",
            "is_vip",
        )
        read_only_fields = fields


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed product view with all fields.
    """
    owner_mini_profile = ProductOwnerMiniProfileSerializer(source="owner")
    comments = CommentSerializer(many=True)
    photos = ProductPhotoSerializer(many=True)

    category = serializers.CharField(source="category.get_parent_category_name", read_only=True)
    subcategory = serializers.CharField(source="category.name", read_only=True)
    city = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "owner_mini_profile",
            "name",
            "category",
            "subcategory",
            "city",
            "price",
            "description",

            "is_new_product",
            "is_delivery_available",
            "is_credit_available",
            "is_barter_available",
            "is_via_negotiator",

            "is_vip",
            "is_premium",
            "is_promoted",
            "is_super_chance",

            "slug",
            "status",
            "is_active",
            "views_count",

            "characteristics",
            "updated_at",
            
            "photos",
            "comments"
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a product with all fields.
    """
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "city",

            "price",
            "description",
            "is_new_product",
            "is_delivery_available",
            "is_credit_available",
            "is_barter_available",
            "is_via_negotiator",

            "characteristics"
        ]
        

class ProductDeleteMultipleSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        help_text="List of product IDs to delete"
    )