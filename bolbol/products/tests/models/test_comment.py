import pytest
from django.contrib.auth import get_user_model
from products.models import Comment, Product

User = get_user_model()

@pytest.mark.django_db
def test_create_comment_with_author_and_product(mocker):
    user = User.objects.create_user(
        phone_number="1234567890",
        password="pass",
        full_name="User One"
    )
    mocker.patch.object(user, "get_masked_fullname", return_value="U. One")
    product = Product.objects.create(name="Prod1", owner=user, price=10.0)  # price əlavə olundu
    comment = Comment.objects.create(
        product=product,
        author=user,
        text="Great product!"
    )
    
    assert comment.masked_author_name == "U. One"
    assert comment.text == "Great product!"
    assert comment.author == user
    assert comment.product == product

@pytest.mark.django_db
def test_create_comment_without_author_sets_masked_name_empty():
    owner = User.objects.create_user(
        phone_number="0987654321",
        password="pass",
        full_name="Owner User"
    )
    product = Product.objects.create(name="Prod2", owner=owner, price=0)  # price əlavə olundu
    comment = Comment.objects.create(product=product, text="Anonymous comment")
    
    assert comment.masked_author_name in [None, ""]

@pytest.mark.django_db
def test_get_masked_author_name_returns_masked_name(mocker):
    user = User.objects.create_user(
        phone_number="1112223333",
        password="pass",
        full_name="User Two"
    )
    mocker.patch.object(user, "get_masked_fullname", return_value="U. Two")
    comment = Comment.objects.create(author=user, text="Hello")
    assert comment.get_masked_author_name() == "U. Two"

@pytest.mark.django_db
def test_get_masked_author_name_returns_anonymous_when_no_author():
    comment = Comment.objects.create(text="No author here")
    assert comment.get_masked_author_name() == "Anonymous"

@pytest.mark.django_db
def test_comments_ordering():
    owner = User.objects.create_user(
        phone_number="2223334444",
        password="pass",
        full_name="Owner User 2"
    )
    product = Product.objects.create(name="Prod3", owner=owner, price=5.0)  # price əlavə olundu
    comment1 = Comment.objects.create(product=product, text="First comment")
    comment2 = Comment.objects.create(product=product, text="Second comment")
    
    comments = list(Comment.objects.filter(product=product))
    # Ordering by "-posted_at", so comment2 should come first
    assert comments[0] == comment2
    assert comments[1] == comment1
