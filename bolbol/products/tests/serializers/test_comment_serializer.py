import pytest
from django.contrib.auth import get_user_model
from products.models import Comment, Product
from products.serializers.comment_serializer import CommentSerializer, CommentCreateSerializer

User = get_user_model()


@pytest.mark.django_db
def test_comment_serializer_with_masked_name(mocker):
    # Create a user and product
    user = User.objects.create(
        full_name="Ali Mammadov",
        phone_number="+994501234567",
        email="ali@example.com"
    )
    product = Product.objects.create(
        name="Test Product",
        owner=user,
        price=10.0
    )
    # Create a comment on the product
    comment = Comment.objects.create(author=user, product=product, text="Very good product!")

    # Mock the name masking function
    mocker.patch("utils.helpers.mask_user_fullname", return_value="A. Mammadov")

    # Serialize the comment
    serializer = CommentSerializer(comment)
    data = serializer.data

    # Check the masked name and content
    assert data["author_masked_fullname"] == "A*** M***"
    assert data["text"] == "Very good product!"
    assert "posted_at" in data


@pytest.mark.django_db
def test_comment_create_serializer_creates_comment():
    # Create a user and product
    user = User.objects.create(
        full_name="Aynur Aliyeva",
        phone_number="+994501234568",
        email="aynur@example.com"
    )
    product = Product.objects.create(
        name="Phone",
        owner=user,
        price=20.5 
    )

    # Create comment via serializer
    serializer = CommentCreateSerializer(
        data={"text": "Great quality!"},
        context={"author": user, "product": product}
    )

    # Validate and save the comment
    assert serializer.is_valid(), serializer.errors
    comment = serializer.save()

    # Check saved data
    assert comment.text == "Great quality!"
    assert comment.author == user
    assert comment.product == product
