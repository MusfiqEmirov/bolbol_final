from django.db import models

__all__ = ("PartnerCompany",)


class PartnerCompany(models.Model):
    logo = models.ImageField(
        verbose_name="Logo",
        upload_to="partners/logos",
    )
    name = models.CharField(
        "Name",
        max_length=255,
        null=True,
        blank=True
    )
    url = models.URLField(
        "Company URL",
        max_length=255
    )
    is_active = models.BooleanField(
        "Is Active",
        default=True
    )

    class Meta:
        verbose_name = "Partner company"
        verbose_name_plural = "Partner companies"

    def __str__(self):
        return f"{self.name} {self.url}"
