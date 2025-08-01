from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    active_products_count = serializers.SerializerMethodField()
    product_count_by_category = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "email",
            "is_active",
            "active_products_count",
            "product_count_by_category"
        )
    
    def get_active_products_count(self, obj):
         return obj.active_products_count
    
    def get_product_count_by_category(self, obj):
        return obj.product_count_by_category


class ProductOwnerMiniProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User mini profile."""
    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "is_shop_profile",
            "active_products_count"
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "email",
        )