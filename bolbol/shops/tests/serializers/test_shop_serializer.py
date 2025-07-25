import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from shops.models import PartnerCompany
from shops.serializers import PartnerCompanySerializer

def get_image_file(name="test.jpg"):
    image = Image.new("RGB", (100, 100), color="white")
    byte_io = BytesIO()
    image.save(byte_io, format="JPEG")
    byte_io.seek(0)
    return SimpleUploadedFile(name, byte_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_partner_company_serializer_valid_data():
    logo = get_image_file()
    data = {
        "name": "Test Company",
        "url": "https://example.com",
        "is_active": True,
        "logo": logo,
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Test Company"
    assert instance.url == "https://example.com"


@pytest.mark.django_db
def test_partner_company_serializer_missing_name():
    logo = get_image_file()
    data = {
        "url": "https://example.com",
        "is_active": True,
        "logo": logo,
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid(), serializer.errors

# Eyni şəkildə digər testlərdə də SimpleUploadedFile əvəzinə get_image_file() istifadə edə bilərsən
