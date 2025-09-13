from typing import Optional
from django.db import models
from django.urls import reverse_lazy
from django.utils.html import mark_safe
from django.db.models import Count
from django.db.models import QuerySet
from products.models import Product

__all__ = (
    "Category",
    "CategoryFilterField"
)


class CategoryQuerySet(models.QuerySet):
    def with_product_counts(self):
        return self.annotate(product_count=Count("products"))


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def with_product_counts(self):
        return self.get_queryset().with_product_counts()
    

class Category(models.Model):
    name = models.CharField(
        "Name", 
        max_length=255, 
        help_text='Warning! Don\'t change this and any other fields here, or it will break the system!'
    )
    icon = models.FileField(
        "Image", 
        upload_to="%Y/%m/%d/categories", 
        null=True, 
        blank=True
    )
    order = models.IntegerField(
        "Display order",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        "Is active", 
        default=True
    )

    is_delivery_enabled = models.BooleanField(
        "Is delivery option enabled", 
        default=True
    )
    is_new_product_enabled = models.BooleanField(
        "Is new product option enabled", 
        default=True
    )
    is_credit_enabled = models.BooleanField(
        "Is credit option enabled", 
        default=True
    )
    is_barter_enabled = models.BooleanField(
        "Is barter option enabled", 
        default=True
    )
    is_negotiator_enabled = models.BooleanField(
        "Is negotiator option enabled", 
        default=True
    )

    parent_category = models.ForeignKey(
        "products.Category",
        verbose_name="Parent category",
        on_delete=models.PROTECT,
        related_name="subcategories",
        related_query_name="subcategory",
        null=True,
        blank=True
    )

    objects = CategoryManager()  # Use the custom manager

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}"

    # @property
    # def product_count(self) -> int:
    #     return getattr(self, "product_count", 0)

    @property
    def is_parent_category(self) -> bool:
        return (self.parent_category is None)

    @property
    def is_subcategory(self) -> bool:
        return (not self.is_subcategory)

    def get_parent_category_name(self) -> str | None:
        if self.parent_category is not None:
            return self.parent_category.name
        return None

    # def get_parent_category_name(self) -> str | None:
    #     return (name := self.parent_category.name) if self.parent_category else None

    def get_category_based_products(self) -> QuerySet[Product]:
        return Product.objects.filter(category=self)

    def get_category_based_products_count(self) -> int:
        return self.get_category_based_products().count()


class CategoryFilterField(models.Model):
    FIELD_TYPE_NUMBER = "number"
    FIELD_TYPE_TEXT = "text"
    FIELD_TYPE_CHOICES = "choices"

    FIELD_TYPES = (
        (FIELD_TYPE_NUMBER, "Number"),
        (FIELD_TYPE_TEXT, "Text"),
        (FIELD_TYPE_CHOICES, "Choices"),
    )

    category = models.ForeignKey(
        "products.Category",
        verbose_name="Category",
        on_delete=models.SET_NULL,
        related_name="category_filter_fields",
        related_query_name="category_filter_field",
        null=True,
        blank=True
    )
    parent_field = models.ForeignKey(
        "self",
        verbose_name="Parent Field",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dependent_fields",
        help_text="The parent field that determines when this field appears."
    )

    field_display_name = models.CharField(
        "Field display name",
        max_length=255,
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
        default=FIELD_TYPE_TEXT,
        null=True,
        blank=True
    )
    choices = models.TextField(
        max_length=255,
        null=True,
        blank=True, 
        help_text="Example: red;green; Warning! Use '‒' instead of normal dash ('-') in brands like: Mercedes‒Benz. Copy ‒"
    )
    order = models.IntegerField(
        "Display order",
        default=0,
        null=True,
        blank=True
    )

    tooltip_text = models.CharField(
        "Tooltip text",
        max_length=64,
        null=True, 
        blank=True, 
    )
    placeholder_text = models.CharField(
        "Placeholder text",
        max_length=64,
        null=True,
        blank=True
    )
    is_hidden_field = models.BooleanField(
        "Hide Field",
        default=False
    )
    max_value_length = models.PositiveSmallIntegerField(
        "Max value length",
        default=16,
        null=True,
        blank=True
    )
    is_required = models.BooleanField(
        "Is required", 
        default=True
    )
    is_autogenerating_product_name = models.BooleanField(
        "Is autogenerating product name",
        default=False
    )

    class Meta:
        verbose_name = "Category Filter Field"
        verbose_name_plural = "Category Filter Fields"
        ordering = ("category",)

    def __str__(self) -> str:
        return f"{self.field_display_name} - {self.type} ({self.category.name})"

    @property
    def has_tooltip(self) -> bool:
        return self.tooltip_text is not None

    # categories = models.ManyToManyField(
    #     Category,
    #     blank=True,
    #     related_name="additional_fields",
    #     related_query_name="additional_field",
    # )
    # # autocomplete_keyword = models.CharField(max_length=122,null=True,blank=True,unique=True)
    # display_name = models.CharField(
    #     max_length=200, help_text="You can change this anytime you want."
    # )
    # dependent_display_name = models.CharField(
    #     null=True, blank=True,
    #     max_length=200, help_text='Field name for dependent options if provided'
    # )
    # name = models.CharField(
    #     max_length=100, help_text="Do not change this name ever! It may brake things"
    # )

    # def __str_(self):
    #     return f"{self.name} - {self.type}"

    # @property
    # def name_dep(self):
    #     return self.name

    # @property
    # def choice_options(self):
    #     return [
    #         choice_option.strip() for choice_option in self.choices.split(";")
    #     ]

    # @property
    # def category_name(self):
    #     if self.categories.all():
    #         return self.categories.all()[0].name

    # @property
    # def normalized_choice_options(self):
    #     options = []
    #     for choice_option in self.choice_options:
    #         if '-' in choice_option:
    #             main_option, _ = choice_option.split('-')
    #             options.append(main_option.strip())
    #         else:
    #             options.append(choice_option.strip())
    #     return options

    # @property
    # def dependent_choice_options(self):
    #     options_list = []
    #     for choice_option in self.choice_options:
    #         if '-' in choice_option:
    #             main_option, dependent_options = choice_option.split('-')
    #             dependent_options_list = [
    #                 dependent_option.strip() 
    #                 for dependent_option in dependent_options.split(',')
    #             ]
    #             for dependent_option in dependent_options_list:
    #                 options_list.append({
    #                     'main': main_option.strip(),
    #                     'option': dependent_option
    #                 })

    #     return options_list


"""
Subkateqoriya -> Category FIlter Fields -> Inner field (CFF based)
Avtomobil -> Marka -> Model
Telefonlar -> Marka -> Model -> Reng, Yaddas, Sim Kart
Telefonlar -> Marka

Marka (Acer, Apple, Aksesuarlar)

Aksesuarlar

Apple -> Model (11) ->

"""