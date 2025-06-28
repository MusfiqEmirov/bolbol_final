from django.db import models

__all__ = ("ProductPhoto",)


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        "products.Product",
        verbose_name="Product",
        on_delete=models.CASCADE,
        related_name="photos",
        related_query_name="photo",
        null=True,
        blank=True
    )
    image = models.ImageField(
        "Image", 
        upload_to="products/photos/%Y/%m/%d"
    )
    order = models.PositiveSmallIntegerField(
        "Order", 
        default=0
    )

    class Meta:
        verbose_name = ("Product photo")
        verbose_name_plural = ("Product photos")
        ordering = ("order",)

    def __str__(self):
        return f"{self.product} photo {self.order}"

    def get_image_url(self) -> str:
        host = "https://konum24.az"
        # if self.image:
        #     return f"{host}/{self.image.url}"
        return f"{host}/uploads/products/photos/2025/02/04/2024-kia-sorento-facelift-3-200x200.jpg"