import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from shops.models import PartnerCompany
from shops.serializers import PartnerCompanySerializer


def get_valid_image_file(name="test.jpg"):
    image = Image.new("RGB", (100, 100), color="white")
    byte_io = BytesIO()
    image.save(byte_io, format="JPEG")
    byte_io.seek(0)
    return SimpleUploadedFile(name, byte_io.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_valid_serializer_data():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "Test Company",
        "url": "https://testcompany.com",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_serializer_missing_logo():
    data = {
        "name": "Company without logo",
        "url": "https://company.com",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert not serializer.is_valid()
    assert "logo" in serializer.errors


@pytest.mark.django_db
def test_serializer_blank_name():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "",
        "url": "https://example.com",
        "is_active": False
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_serializer_missing_url():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "TestCo",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert not serializer.is_valid()
    assert "url" in serializer.errors


@pytest.mark.django_db
def test_serializer_with_invalid_url():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "Invalid URL Co",
        "url": "not-a-url",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert not serializer.is_valid()
    assert "url" in serializer.errors


@pytest.mark.django_db
def test_serializer_with_null_name():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": None,
        "url": "https://valid.com",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_serializer_save_creates_instance():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "Save Test",
        "url": "https://savetest.com",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert PartnerCompany.objects.filter(id=instance.id).exists()


@pytest.mark.django_db
def test_serialize_existing_instance():
    logo = get_valid_image_file()
    instance = PartnerCompany.objects.create(
        logo=logo,
        name="Serialize Me",
        url="https://serialize.com",
        is_active=True
    )
    serializer = PartnerCompanySerializer(instance)
    data = serializer.data
    assert data["name"] == "Serialize Me"
    assert data["url"] == "https://serialize.com"
    assert data["is_active"] is True


@pytest.mark.django_db
def test_update_serializer():
    logo1 = get_valid_image_file("logo1.jpg")
    logo2 = get_valid_image_file("logo2.jpg")

    instance = PartnerCompany.objects.create(
        logo=logo1,
        name="Old Name",
        url="https://old.com",
        is_active=True
    )

    data = {
        "logo": logo2,
        "name": "New Name",
        "url": "https://new.com",
        "is_active": False
    }
    serializer = PartnerCompanySerializer(instance, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_instance = serializer.save()
    assert updated_instance.name == "New Name"
    assert updated_instance.url == "https://new.com"
    assert updated_instance.is_active is False


@pytest.mark.django_db
def test_serializer_max_length_violation():
    logo = get_valid_image_file()
    data = {
        "logo": logo,
        "name": "A" * 300,  # exceeds max_length
        "url": "https://example.com",
        "is_active": True
    }
    serializer = PartnerCompanySerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
