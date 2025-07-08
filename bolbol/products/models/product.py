from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.configs import ProductConfig
from utils.helpers import shrink_text, generate_slug
from django.urls import reverse

__all__ = ("Product",)




class Product(models.Model):
    PREMIUM = "pre"
    VIP = "vip"
    PROMOTED = "pro"
    SIMPLE = "sim"

    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    PRODUCT_STATUSES = (
        (PENDING, ("Pending")),
        (APPROVED, ("Approved")),
        (REJECTED, ("Rejected")),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner",
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="product",
        null=True,
        blank=True
    )

    name = models.CharField(
        "Name", 
        max_length=255,
    )

    category = models.ForeignKey(
        "products.Category",
        verbose_name="Category",
        on_delete=models.PROTECT,
        related_name="category_products",
        related_query_name="category_product",
        null=True,
        blank=True
    )

    city = models.ForeignKey(
        "products.City",
        verbose_name="City",
        on_delete=models.PROTECT,
        related_name="products",
        related_query_name="product",
        null=True,
        blank=True
    )
    price = models.DecimalField(
        "Price", 
        max_digits=20, 
        decimal_places=2,
        validators=[
            MinValueValidator(ProductConfig.PRODUCT_MIN_PRICE),
            MaxValueValidator(ProductConfig.PRODUCT_MAX_PRICE)
        ]
    )
    description = models.TextField(
        "Description", 
        max_length=3000, 
        null=True, 
        blank=True
    )

    is_new_product = models.BooleanField(
        "Is new product", 
        default=False
    )
    is_delivery_available = models.BooleanField(
        "Is delivery available",
        default=False
    )
    is_credit_available = models.BooleanField(
        "Is credit available", 
        default=False
    )
    is_barter_available = models.BooleanField(
        "Is barter available", 
        default=False
    )
    is_via_negotiator = models.BooleanField(
        "Is via negotiator", 
        default=False
    )

    is_vip = models.BooleanField(
        "Is vip",
        default=False, 
        db_index=True
    )
    is_premium = models.BooleanField(
        "Is premium", 
        default=False, 
        db_index=True
    )
    is_promoted = models.BooleanField(
        "Is promoted", 
        default=False, 
        db_index=True
    )
    is_super_chance = models.BooleanField(
        "Is super chance", 
        default=False, 
        db_index=True
    )

    status = models.IntegerField(
        "Status", 
        choices=PRODUCT_STATUSES, 
        default=PENDING,
        null=True,
        blank=True    
    )
    is_active = models.BooleanField(
        "Is active", 
        default=False
    )
    characteristics = models.JSONField(
        null=True,
        blank=True
    )
    views_count = models.PositiveIntegerField(
        "Views count", 
        default=0
    )
    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        "Created at", 
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        "Updated at", 
        auto_now=True,
        null=True,
        blank=True
    )
    expires_at = models.DateTimeField(
        "Expires at", 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-updated_at",)

    def __str__(self) -> str:
        return shrink_text(self.name, 25)

    # def save(self, *args, **kwargs):
    #     if not self.pk:  
    #         super().save(*args, **kwargs)

    #     if not self.slug:
    #         self.slug = f"{self.pk}-{generate_slug(self.name)}"

    #     return super().save(*args, **kwargs)

    @property
    def title(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("apis:product-detail", kwargs={"product_slug": self.slug})

    def get_thumbnail_photo_url(self) -> str:
        return self.photos.first().image.url

    def get_comments_count(self) -> int:
        return self.comments.count()

    def get_preview_photo_url(self) -> str:
        preview_photo = self.photos.filter(order=0).first()
        # if preview_photo:
        #     return preview_photo.image.url

        host = "https://konum24.az"
        return f"{host}/uploads/products/photos/2025/02/04/2024-kia-sorento-facelift-3-200x200.jpg"

    def deactivate(self, commit=True) -> None:
        self.is_active = False
        if commit:
            self.save()