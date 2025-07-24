import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from products.models import Product, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_get_comments_by_product():
    client = APIClient()
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0, slug="test-product", is_active=True)
    comment = Comment.objects.create(author=user, product=product, text="Test comment")

    url = reverse("apis:product-comments", kwargs={"product_slug": product.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["text"] == "Test comment"

@pytest.mark.django_db
def test_create_comment_authenticated():
    client = APIClient()
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0, slug="test-product", is_active=True)

    client.force_authenticate(user=user)

    url = reverse("apis:comment-create", kwargs={"product_slug": product.slug})
    data = {"text": "New comment"}

    response = client.post(url, data)

    assert response.status_code == 201
    assert response.json()["text"] == "New comment"
    assert Comment.objects.filter(product=product, author=user, text="New comment").exists()

@pytest.mark.django_db
def test_create_comment_unauthenticated():
    client = APIClient()
    # Burada user yaradıb product-a owner kimi veririk,
    # amma client authenticate edilmir, yəni anonimdir
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(
        name="Test Product",
        owner=user,  # None deyil!
        price=10.0,
        slug="test-product",
        is_active=True
    )

    url = reverse("apis:comment-create", kwargs={"product_slug": product.slug})
    data = {"text": "New comment"}

    response = client.post(url, data)

    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_comment_authenticated_owner():
    client = APIClient()
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0, slug="test-product", is_active=True)
    comment = Comment.objects.create(author=user, product=product, text="To be deleted")

    client.force_authenticate(user=user)
    url = reverse("apis:delete-comment", kwargs={"comment_id": comment.id})

    response = client.delete(url)

    assert response.status_code == 204
    assert not Comment.objects.filter(id=comment.id).exists()

@pytest.mark.django_db
def test_delete_comment_authenticated_not_owner():
    client = APIClient()
    user1 = User.objects.create_user(phone_number="1111111111", password="testpass")
    user2 = User.objects.create_user(phone_number="2222222222", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user1, price=10.0, slug="test-product", is_active=True)
    comment = Comment.objects.create(author=user1, product=product, text="User1 comment")

    client.force_authenticate(user=user2)
    url = reverse("apis:delete-comment", kwargs={"comment_id": comment.id})

    response = client.delete(url)

    assert response.status_code == 404  # Not found because filter(author=user2) doesn't find the comment

@pytest.mark.django_db
def test_delete_comment_unauthenticated():
    client = APIClient()
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0, slug="test-product", is_active=True)
    comment = Comment.objects.create(author=user, product=product, text="To be deleted")

    url = reverse("apis:delete-comment", kwargs={"comment_id": comment.id})

    response = client.delete(url)

    assert response.status_code == 401  # Unauthorized
