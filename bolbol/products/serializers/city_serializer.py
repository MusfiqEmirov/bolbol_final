from rest_framework import serializers
from products.models import City


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model, used for listing cities."""
    class Meta:
        model = City
        fields = (
            "id",
            "name"
        )