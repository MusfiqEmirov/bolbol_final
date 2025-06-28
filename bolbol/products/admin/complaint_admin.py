from django.contrib import admin
from django.utils.html import format_html
from products.models import Complaint, ComplaintCategory


@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "priority_level", "colored_priority_display")
    list_filter = ("priority_level",)
    search_fields = ("name", "description")
    ordering = ("priority_level", "name")

    def colored_priority_display(self, obj):
        color_map = {
            "green": "#4CAF50",
            "yellow": "#FFC107",
            "red": "#F44336",
        }
        return format_html(
            '<span style="color: {}">{}</span>',
            color_map.get(obj.priority_level, "#000"),
            obj.get_priority_level_display()
        )
    
    colored_priority_display.short_description = "Priority Level"

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("complained_at", "complainant", "category", "product", "short_text")
    list_filter = ("category", "complained_at")
    search_fields = ("complainant__username", "text", "product__name")
    autocomplete_fields = ("complainant", "category", "product")
    readonly_fields = ("complained_at",)
    ordering = ("-complained_at",)
    actions = ["mark_as_resolved"]

    def short_text(self, obj):
        return obj.text[:50] + "..." if obj.text and len(obj.text) > 50 else obj.text
    
    short_text.short_description = "Complaint Text"

    def mark_as_resolved(self, request, queryset):
        queryset.update(category=None)  # Example action to reset category
        self.message_user(request, "Selected complaints marked as resolved.")
    
    mark_as_resolved.short_description = "Mark selected complaints as resolved"
