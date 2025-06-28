from rest_framework import serializers
from products.models import ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source="get_image_url", read_only=True)

    class Meta:
        model = ProductPhoto
        fields = (
            "order",
            "image_url"
        )


class ProductPhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = [
            "image",
            "order"
        ]