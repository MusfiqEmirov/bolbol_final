import pytest
from products.models import Category, CategoryFilterField
from model_bakery import baker


@pytest.mark.django_db
def test_category_str_representation():
    category = Category.objects.create(name="Elektronika")
    assert str(category) == "Elektronika"

@pytest.mark.django_db
def test_category_is_parent_and_subcategory_properties():
    parent = Category.objects.create(name="Telefonlar")
    child = Category.objects.create(name="iPhone", parent_category=parent)

    assert parent.is_parent_category is True
    assert child.is_parent_category is False
    assert child.get_parent_category_name() == "Telefonlar"

@pytest.mark.django_db
def test_category_get_category_based_products_count_returns_zero():
    category = Category.objects.create(name="Kompüterlər")
    assert category.get_category_based_products_count() == 0


@pytest.mark.django_db
def test_category_filter_field_str_and_properties():
    category = Category.objects.create(name="Telefonlar")
    field = CategoryFilterField.objects.create(
        category=category,
        field_display_name="Marka",
        type=CategoryFilterField.FIELD_TYPE_CHOICES,
        tooltip_text="Markanı seçin",
    )

    assert str(field) == "Marka - choices (Telefonlar)"
    assert field.has_tooltip is True

@pytest.mark.django_db
def test_category_filter_field_without_tooltip():
    category = Category.objects.create(name="TV")
    field = CategoryFilterField.objects.create(
        category=category,
        field_display_name="Model",
        type=CategoryFilterField.FIELD_TYPE_TEXT,
    )

    assert field.has_tooltip is False


@pytest.mark.django_db
def test_subcategory_with_filters():
    parent = Category.objects.create(name="Telefonlar")
    child = Category.objects.create(name="Apple", parent_category=parent)
    
    filter_field = CategoryFilterField.objects.create(
        category=child,
        field_display_name="Model",
        type=CategoryFilterField.FIELD_TYPE_TEXT,
    )

    assert filter_field.category.name == "Apple"
    assert filter_field.field_display_name == "Model"
