from django.conf import settings
from django.db import models
from utils.validators import validate_phone_number
from utils.constants import TimeIntervals

from products.models import Product

__all__ = (
    "Shop",
    "ShopContact",
    "ShopWorkingHours"
)


class Shop(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(
        "Name",
        max_length=255,
        null=True,
        blank=True
    )
    activities = models.ManyToManyField(
        "shops.ShopActivity", 
        verbose_name="Shop Activities"
    )
    # slogan = models.CharField(
    #     "Slogan", 
    #     max_length=255, 
    #     null=True, 
    #     blank=True
    # )
    logo = models.ImageField(
        "Logo",
        max_length=255,
        upload_to="shops/logos/%Y/%m/%d",
        null=True,
        blank=True
    )
    address = models.TextField(
        "Address",
        max_length=255,
        null=True, 
        blank=True
    )
    bio = models.TextField(
        "Intro text",
        null=True,
        blank=True
    )

    city = models.ForeignKey(
        "products.City",
        verbose_name="City",
        on_delete=models.PROTECT,
        related_name="shops",
        related_query_name="shop",
        null=True,
        blank=True
    )

    background_image = models.ImageField(
        "Background image",
        upload_to="shops/background/%Y/%m/%d",
        null=True,
        blank=True
    )
    map_link = models.URLField(
        "Map location link",
        max_length=255,
        null=True, 
        blank=True
    )
    map_latitude = models.FloatField(
        "Map location latitude", 
        null=True, 
        blank=True
    )
    map_longitude = models.FloatField(
        "Map location longitude", 
        null=True, 
        blank=True
    )

    is_active = models.BooleanField(
        "Is active", 
        default=True
    )

    created_at = models.DateTimeField(
        "Created at", 
        auto_now_add=True, 
        db_index=True
    )
    updated_at = models.DateTimeField(
        "Updated at", 
        auto_now=True
    )
    shop_working_hours_data = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
    
    @property
    def get_product_count(self):
        return Product.objects.filter(owner=self.owner).count()

    def __str__(self):
        return f"{self.name}"


class ShopContact(models.Model):
    shop = models.ForeignKey(
        Shop,
        verbose_name="Shop",
        on_delete=models.CASCADE,
        related_name="contacts",
        related_query_name="contact",
    )
    phone_number = models.CharField(
        "Phone number", 
        max_length=255, 
        validators=[validate_phone_number],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Shop contact"
        verbose_name_plural = "Shop contacts"

    def __str__(self):
        return f"{self.phone_number}"


class ShopWorkingHours(models.Model):
    shop = models.ForeignKey(
        Shop,
        verbose_name="Shop",
        on_delete=models.CASCADE,
        related_name="working_hours",
        related_query_name="working_hour"
    )
    day_of_week = models.CharField(
        max_length=9, 
        choices=TimeIntervals.WEEKDAYS,
        null=True,
        blank=True
    )
    opening_time = models.TimeField(
        "Opening Time",
        null=True,
        blank=True
    )
    closing_time = models.TimeField(
        "Closing Time",
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ("shop", "day_of_week")

    def __str__(self):
        return f"{self.shop.name} - {self.day_of_week}: {self.opening_time} to {self.closing_time}"
    
