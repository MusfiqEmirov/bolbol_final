from django.contrib import admin
from shops.models import ShopRegistrationRequest


@admin.register(ShopRegistrationRequest)
class ShopRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ("shop_owner_full_name", "shop_name", "shop_owner", "status", "get_shop_activities", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "status")
    search_fields = ("shop_owner__username", "shop_name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Shop Owner Information", {
            "fields": ("shop_owner",)
        }),
        ("Shop Details", {
            "fields": ("shop_name", "shop_activities", "status")  # Add shop_activities here
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )
    ordering = ("-created_at",)

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_shop_activities(self, obj):
        return ", ".join([activity.name for activity in obj.shop_activities.all()])
    
    get_shop_activities.short_description = "Shop Activities"

    