from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.validators import validate_phone_number
from utils.helpers import mask_user_fullname
from .user_manager import UserManager


class User(AbstractUser):
    DEFAULT_FULL_NAME = "Anonymous User"

    username = None
    first_name = None
    last_name = None

    full_name = models.CharField(
        "Full Name",
        max_length=255,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        "Phone Number",
        max_length=13, 
        unique=True, 
        null=True,
        blank=True,
        validators=[validate_phone_number]
    )
    email = models.EmailField(
        "Email address",
        null=True, 
        blank=True,
        unique=True
    )

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.phone_number}"

    def get_masked_fullname(self):
        return mask_user_fullname(self.full_name)

    def is_shop_profile(self):
        from shops.models import Shop
        return Shop.objects.filter(owner=self).exists()

    @property
    def active_products_count(self):
        from products.models import Product
        return Product.objects.filter(owner=self, is_active=True).count()