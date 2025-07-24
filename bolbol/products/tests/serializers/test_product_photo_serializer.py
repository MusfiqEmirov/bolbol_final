import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import ProductPhoto
from products.serializers.product_photo_serializer import ProductPhotoSerializer, ProductPhotoCreateSerializer


@pytest.mark.django_db
def test_product_photo_serializer():
    # Simulate uploading an image file
    image_file = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"fake-image-content",
        content_type="image/jpeg"
    )
    
    photo = ProductPhoto.objects.create(
        image=image_file,
        order=1
    )
    
    serializer = ProductPhotoSerializer(photo)
    data = serializer.data
    
    assert "order" in data
    assert data["order"] == 1
    assert "image_url" in data
    assert isinstance(data["image_url"], str) 
