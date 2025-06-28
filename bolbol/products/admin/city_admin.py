from django.contrib import admin
from products.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "is_pinned", "order")
    list_editable = ("is_active", "is_pinned", "order")
    list_filter = ("is_active", "is_pinned")
    search_fields = ("name",)
    ordering = ("-is_pinned", "order", "name")
    fieldsets = (
        (None, {
            "fields": ("name",)
        }),
        ("Status", {
            "fields": ("is_active", "is_pinned"),
            "description": "Set the active and pinned status of the city."
        }),
        ("Ordering", {
            "fields": ("order",),
            "description": "Specify the order in dropdowns or lists."
        }),
    )
    empty_value_display = "-empty-"