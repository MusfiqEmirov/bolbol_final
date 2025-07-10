from rest_framework import serializers
from products.models import ReactivationRequest


class ReactivationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactivationRequest
        fields = [
            "id",
            "product",
            "user",
            "status",
            "created_at",
            "admin_note",
        ]
        read_only_fields = ["id", "created_at", "user"]