from django.contrib import admin
from shops.models import ShopActivity


@admin.register(ShopActivity)
class ShopActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_per_page = 20