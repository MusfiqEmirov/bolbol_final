from django.db import models


__all__ = ("City",)

class City(models.Model):
    name = models.CharField(
        "Name", 
        max_length=255,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        "Is active", 
        default=True
    )
    is_pinned = models.BooleanField(
        "Is pinned", 
        default=False, 
        help_text="Shown as main city in footer"
    )
    order = models.PositiveSmallIntegerField(
        "Order", 
        default=0,
        help_text="Order of cities in dropdown",
        unique=True
    )

    class Meta:
        verbose_name = ("City")
        verbose_name_plural = ("Cities")
        ordering = ("is_pinned", "order")

    def __str__(self):
        """Returns the name of the city as its string representation."""
        return self.name