from django.contrib import admin
from django.utils.html import format_html
from products.models import ProductPhoto


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "product", 
        "image_preview", 
        "order"
    )
    list_editable = ("order",)
    list_filter = ("product",)
    search_fields = ("product__name",)
    ordering = ("order",)
    readonly_fields = ("image_preview",)

    fieldsets = (
        (
            "Photo Information", 
            {
                "fields": (
                    "product", 
                    "order", 
                    "image", 
                    "image_preview"
                ),
            },
        ),
    )

    def image_preview(self, obj):
        """Displays a preview of the image in the admin panel."""
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius:5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"