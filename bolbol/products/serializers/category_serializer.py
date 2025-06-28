from rest_framework import serializers
from products.models import Category, CategoryFilterField


# class CategorySerializer(serializers.ModelSerializer):
#     """Serializer for the Category model with main_category name and ID fields."""
#     # main_category = serializers.CharField(source="main_category.name", read_only=True)
#     # main_category_id = serializers.IntegerField(source="main_category.pk", read_only=True)

#     class Meta:
#         model = Category
#         fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model, including subcategories for parent categories."""
    parent_category_id = serializers.IntegerField(source="parent_category.pk", read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "order",
            "is_active",
            "is_delivery_enabled",
            "is_new_product_enabled",
            "is_credit_enabled",
            "is_barter_enabled",
            "is_negotiator_enabled",
            "parent_category_id",
            "subcategories"
        ]

    def get_subcategories(self, obj):
        """Retrieve subcategories for the given parent category."""
        subcategories = obj.subcategories.filter(is_active=True)
        return CategorySerializer(subcategories, many=True).data


class SubcategorySerializer(serializers.ModelSerializer):
    parent_category_id = serializers.IntegerField(source="parent_category.pk", read_only=True)
    products_count = serializers.IntegerField(source="get_category_based_products_count", read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "order",
            "parent_category_id",
            "products_count"
        )