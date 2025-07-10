from django.db import models
from django.conf import settings


class ProductUpdateRequest(models.Model):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )
    user_data = models.JSONField(null=True, blank=True)
    photo_meta = models.JSONField(null=True, blank=True)

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="update_requests")
    data = models.JSONField()  
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = ("Product update request")
        verbose_name_plural = ("Product update requests")


class ReactivationRequest(models.Model):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    PRODUCT_STATUSES = (
        (PENDING, ("Pending")),
        (APPROVED, ("Approved")),
        (REJECTED, ("Rejected")),
    )

    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.CASCADE, 
        related_name="reactivation_requests"
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    status = models.IntegerField(
        max_length=10, 
        choices=PRODUCT_STATUSES, 
        default=PENDING
        )
    created_at = models.DateTimeField(auto_now_add=True)
    admin_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reactivation request for {self.product} by {self.user}"
    
    class Meta:
        verbose_name = ("Reactivation request")
        verbose_name_plural = ("Reactivation requests")


