from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "email",
            "is_active"
        )


class ProductOwnerMiniProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User mini profile."""
    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "is_shop_profile",
            "available_products_count"
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