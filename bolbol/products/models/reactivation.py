from django.db import models
from django.conf import settings


__all__ = ("ReactivationRequest",)

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