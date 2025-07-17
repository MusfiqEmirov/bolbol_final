from rest_framework import serializers
from shops.models import(
    Shop,
    ShopContact,
    ShopWorkingHours, 
    ShopRegistrationRequest, 
    ShopActivity
)


# class ShopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = "__all__"


class ShopContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopContact
        fields = ["phone_number"]


class ShopWorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopWorkingHours
        fields = [
            "day_of_week",
            "opening_time", 
            "closing_time"
        ]


class ShopSerializer(serializers.ModelSerializer):
    contacts = ShopContactSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Shop
        fields = [
            "id",
            "name",
            "logo",
            "city_name",
            "is_active",
            "contacts",
            "product_count", 
        ]
    
    def get_product_count(self, obj):
        return obj.get_product_count


class ShopDetailSerializer(serializers.ModelSerializer):
    contacts = ShopContactSerializer(many=True, read_only=True)
    working_hours = ShopWorkingHoursSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

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
            "working_hours",
            "created_at",
            "updated_at",
            "contacts",
            "product_count", 
        ]
        
    def get_product_count(self, obj):
        return obj.get_product_count


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