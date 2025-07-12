from rest_framework import serializers
from shops.models import Shop, ShopRegistrationRequest
from shops.models import ShopActivity


# class ShopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "logo",
            "city_name",
            "is_active",
        ]


class ShopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "logo",
            "background_image",
            "bio",
            "address",
            "city_name",
            "map_link",
            "map_latitude",
            "map_longitude",
            "is_active",
            "activities",
            "shop_working_hours_data",
            "created_at",
            "updated_at",
        ]


class ShopRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRegistrationRequest
        fields = (
            "shop_owner_full_name",
            "shop_name",
            "shop_activities",
        )


class ShopActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopActivity
        fields = (
            "id", 
            "name"
        )


class ShopUpdateSerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(
        queryset=ShopActivity.objects.all(),
        many=True
    )

    class Meta:
        model = Shop
        fields = ( 
            "logo",
            "background_image",
            "name",
            "activities",
            "bio",
            "city",
            "address",
            "map_link",
            "shop_working_hours_data"
        )