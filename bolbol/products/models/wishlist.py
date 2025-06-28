from django.db import models
from django.conf import settings

__all__ = ("Wishlist",)


class Wishlist(models.Model):
    """Model to store user's bookmarked products."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="wishlists",
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.CASCADE, 
        related_name="wishlisted_by",
        null=True,
        blank=True
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user} - {self.product.name}"