from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = (
        "__str__",
        "owner",
        "category__name",
        "city",
        "price",
        "is_new_product",
        "is_delivery_available",
        "is_credit_available",
        "is_barter_available",
        "is_vip",
        "is_premium",
        "is_promoted",
        "status",
        "views_count",
        "created_at",
        "updated_at",
    )
    # Fields to make clickable links
    list_display_links = ("__str__",)
    # Fields to filter the list view
    list_filter = (
        "is_new_product",
        "is_delivery_available",
        "is_credit_available",
        "is_barter_available",
        "is_vip",
        "is_premium",
        "is_promoted",
        "status",
        "created_at",
        "city",
        "category",
    )
    # Fields to enable search functionality
    search_fields = ("name", "description", "owner__ownername", "city__name", "category__name")
    # Fields to make editable directly in the list view
    list_editable = (
        # "is_new_product",
        # "is_delivery_available",
        # "is_credit_available",
        # "is_barter_available",
        # "is_vip",
        # "is_premium",
        # "is_promoted",
        # "status",
    )
    # Default ordering in the list view
    ordering = ("-created_at",)
    # Fields to group in the detail view
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "owner", "category", "city", "price", "description"),
        }),
        ("Status and Promotion", {
            "fields": (
                "is_new_product", "is_delivery_available", "is_credit_available", "is_barter_available",
                "is_vip", "is_premium", "is_promoted", "is_super_chance", "status", "is_active"
            ),
        }),
        ("Metadata", {
            "fields": ("views_count", "characteristics", "created_at", "updated_at", "expires_at"),
        }),
    )
    # Fields that are read-only
    readonly_fields = ("created_at", "updated_at", "views_count")

    # Actions for bulk updates
    actions = ["mark_as_approved", "mark_as_rejected"]

    def mark_as_approved(self, request, queryset):
        queryset.update(status=Product.APPROVED)
        self.message_owner(request, "Selected products have been marked as approved.")
    mark_as_approved.short_description = "Mark selected products as Approved"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status=Product.REJECTED)
        self.message_owner(request, "Selected products have been marked as rejected.")
    mark_as_rejected.short_description = "Mark selected products as Rejected"