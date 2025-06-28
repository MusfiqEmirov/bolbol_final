from django.contrib import admin
from products.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "get_masked_author_name", 
        "product", 
        "text_excerpt", 
        "posted_at"
    )
    list_filter = ("posted_at", "product")
    search_fields = ("text", "author__username", "author__email", "product__name")
    date_hierarchy = "posted_at"
    ordering = ("-posted_at",)
    list_per_page = 20

    def text_excerpt(self, obj):
        """Display a truncated version of the text for better readability."""
        return obj.text[:50] + "..." if obj.text and len(obj.text) > 50 else obj.text

    text_excerpt.short_description = "Comment Excerpt"

    def get_queryset(self, request):
        """Optimize the query by selecting related fields."""
        queryset = super().get_queryset(request)
        return queryset.select_related("author", "product")

    def get_masked_author_name(self, obj):
        """Display the masked author name if available."""
        return obj.get_masked_author_name()

    get_masked_author_name.short_description = "Author Name"