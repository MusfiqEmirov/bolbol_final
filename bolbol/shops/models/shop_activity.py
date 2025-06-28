from django.db import models

__all__ = ("ShopActivity",)


class ShopActivity(models.Model):
    name = models.CharField(
        "Name",
        max_length=64,
        unique=True,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        "Is active",
        default=True
    )

    class Meta:
        verbose_name = "Shop Activity"
        verbose_name_plural = "Shop Activities"

    def __str__(self):
        return self.name