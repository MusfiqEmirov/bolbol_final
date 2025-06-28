from django.db import models
from django.conf import settings

from utils.helpers import shrink_text
from utils.configs import ComplaintConfig

__all__ = (
    "Complaint",
    "ComplaintCategory",
)


class ComplaintCategory(models.Model):
    COMPLAINT_PRIORITY_CHOICES = [
        ("green", "🟢 Green (Low Priority)"),
        ("yellow", "🟡 Yellow (Medium Priority)"),
        ("red", "🔴 Red (High Priority)"),
    ]

    name = models.CharField(
        max_length=100, 
        verbose_name="Category Name", 
        help_text="The name of the complaint category."
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Description", 
        help_text="A brief description of the complaint category."
    )
    priority_level = models.CharField(
        max_length=6, 
        choices=COMPLAINT_PRIORITY_CHOICES, 
        default="green", 
        verbose_name="Priority Level", 
        help_text="The priority level of this complaint category."
    )

    class Meta:
        verbose_name = "Complaint Category"
        verbose_name_plural = "Complaint Categories"

    def __str__(self):
        return f"{self.name} {self.get_priority_level_display()}"


class Complaint(models.Model):
    product = models.ForeignKey(
        "products.Product",
        verbose_name="Product",
        on_delete=models.SET_NULL,
        related_name="complaints",
        related_query_name="complaint",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        ComplaintCategory, 
        on_delete=models.SET_NULL, 
        verbose_name="Category", 
        null=True,
        blank=True,
        help_text="The category of the complaint."
    )
    complainant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Author",
        on_delete=models.SET_NULL,
        related_name="complaints",
        related_query_name="complaint",
        null=True,
        blank=True
    )
    text = models.TextField(
        "Text",
        max_length=ComplaintConfig.COMPLAINT_BODY_TEXT_SYM_LIMIT,
        null=True,
        blank=True
    )
    complained_at = models.DateTimeField(
        "Complained at",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ("-complained_at",)

    def __str__(self) -> str:
        return shrink_text(self.text)