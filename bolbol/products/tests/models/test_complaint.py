import pytest
from django.contrib.auth import get_user_model
from products.models import Product
from products.models.complaint import Complaint, ComplaintCategory
from utils.helpers import shrink_text

User = get_user_model()

@pytest.mark.django_db
def test_create_complaint_category():
    category = ComplaintCategory.objects.create(
        name="Shipping",
        description="Issues related to shipping",
        priority_level="yellow"
    )
    assert category.name == "Shipping"
    assert category.description == "Issues related to shipping"
    assert category.priority_level == "yellow"
    # Test __str__ output contains name and priority display string
    assert "Shipping" in str(category)
    assert "Yellow" in str(category)  # "Yellow (Medium Priority)"'in qisaldılmış versiyası

@pytest.mark.django_db
def test_create_complaint_with_all_fields():
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0)  # price əlavə edildi
    category = ComplaintCategory.objects.create(name="Quality", priority_level="red")
    
    complaint_text = "This product is damaged."
    complaint = Complaint.objects.create(
        product=product,
        category=category,
        complainant=user,
        text=complaint_text
    )
    
    assert complaint.product == product
    assert complaint.category == category
    assert complaint.complainant == user
    assert complaint.text == complaint_text
    assert complaint.complained_at is not None
    
    # Test __str__ uses shrink_text
    assert str(complaint) == shrink_text(complaint_text)

@pytest.mark.django_db
def test_create_complaint_without_optional_fields():
    # Can create complaint without product, category, complainant, text (all nullable/blank=True)
    complaint = Complaint.objects.create()
    assert complaint.product is None
    assert complaint.category is None
    assert complaint.complainant is None
    assert complaint.text in [None, ""]

@pytest.mark.django_db
def test_complaints_ordering():
    user = User.objects.create_user(phone_number="1112223333", password="testpass")
    product = Product.objects.create(name="Ordering Product", owner=user, price=15.0)  # price əlavə edildi
    complaint1 = Complaint.objects.create(product=product, complained_at="2023-01-01T10:00:00Z")
    complaint2 = Complaint.objects.create(product=product, complained_at="2023-01-02T10:00:00Z")
    
    complaints = list(Complaint.objects.filter(product=product))
    # Default ordering is by -complained_at, so complaint2 first
    assert complaints[0] == complaint2
    assert complaints[1] == complaint1