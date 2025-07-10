from django.utils import timezone
from datetime import timedelta
from django.contrib import admin

from products.models import Product
from products.models import ReactivationRequest
from products.tasks import send_product_approved_email_task

@admin.action(description="Approve reactivation and activate product")
def approve_selected_requests(modeladmin, request, queryset):
    for req in queryset.filter(status=ReactivationRequest.PENDING):
        req.status = ReactivationRequest.APPROVED
        req.product.is_active = True
        req.product.save()
        req.save()

@admin.register(ReactivationRequest)
class ReactivationRequestAdmin(admin.ModelAdmin):
    list_display = ("product", "status", "created_at")
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status == ReactivationRequest.APPROVED:
            product = obj.product
            product.is_active = True
            product.status = Product.APPROVED
            product.expires_at = timezone.now() + timedelta(days=30)
            product.save()

            send_product_approved_email_task.delay(product.owner.email, product.slug)
            obj.delete()  
