from django.contrib import admin
from products.models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Wishlist model.
    """
    list_display = ("user", "product", "added_at")  # Show these fields in the list view
    list_filter = ("added_at",)  # Filter by the added date
    search_fields = ("user__username", "product__name")  # Enable searching by user or product name
    autocomplete_fields = ("user", "product")  # Enable autocomplete for related fields
    date_hierarchy = "added_at"  # Add a navigation bar by date for the 'added_at' field
    ordering = ("-added_at",)  # Order by most recently added items
    list_per_page = 25  # Limit the number of items displayed per page
    readonly_fields = ("added_at",)

    def get_queryset(self, request):
        """
        Customize the queryset for better performance or additional filtering.
        """
        qs = super().get_queryset(request)
        return qs.select_related("user", "product")  # Use select_related to optimize database queries