from django.contrib import admin
from django.utils.html import format_html
from products.models import Category, CategoryFilterField


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "parent_category__name",
        "icon_preview",
        "order",
        "is_active",
        "is_delivery_enabled",
        "is_new_product_enabled",
        "is_credit_enabled",
        "is_barter_enabled",
        "is_negotiator_enabled"
    )
    list_editable = (
        # "order", 
        # "is_active", 
        # "is_delivery_enabled", 
        # "is_new_product_enabled", 
        # "is_credit_enabled", 
        # "is_barter_enabled", 
        # "is_negotiator_enabled"
    )
    list_filter = ("is_active", "is_delivery_enabled", "parent_category")
    search_fields = ("name",)
    ordering = ("order", "name")
    readonly_fields = ("icon_preview",)
    fieldsets = (
        (
            "General Information", 
            {
                "fields": (
                    "name", 
                    "parent_category", 
                    "order", 
                    "is_active", 
                    "icon", 
                    "icon_preview"
                ),
            },
        ),
        (
            "Feature Toggles", 
            {
                "fields": (
                    "is_delivery_enabled", 
                    "is_new_product_enabled", 
                    "is_credit_enabled", 
                    "is_barter_enabled", 
                    "is_negotiator_enabled"
                ),
            },
        ),
    )

    def icon_preview(self, obj):
        """Show a preview of the uploaded icon in the admin."""
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.icon.url)
        return "No Icon"
    icon_preview.short_description = "Icon Preview"


@admin.register(CategoryFilterField)
class CategoryFilterFieldAdmin(admin.ModelAdmin):
    list_display = (
        "field_display_name",
        "category",
        "type",
        "order",
        "is_hidden_field",
        "is_required",
    )
    list_filter = ("category", "type", "is_hidden_field", "is_required")
    search_fields = ("field_display_name", "category__name", "tooltip_text", "placeholder_text")
    ordering = ("order",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("category", "field_display_name", "type", "order"),
            "description": "Basic details about the filter field."
        }),
        ("Field Configuration", {
            "fields": ("choices", "max_value_length", "placeholder_text", "tooltip_text"),
            "description": "Configure how the field behaves and what values it can accept."
        }),
        ("Display Settings", {
            "fields": ("is_hidden_field", "is_required", "is_autogenerating_product_name"),
            "description": "Control whether the field is hidden or required.",
        }),
    )

    save_on_top = True  # Show save buttons on top for convenience