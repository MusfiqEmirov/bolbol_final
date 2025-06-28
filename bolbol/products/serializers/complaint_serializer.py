from rest_framework import serializers
from products.models import Complaint, ComplaintCategory


class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory
        exclude = (
            "priority_level", 
            "description"
        )


class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = (
            "product",
            "category",
            "text"
        )