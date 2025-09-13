import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from shops.models import PartnerCompany


@pytest.mark.django_db
def test_create_partner_company_minimal():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")

    company = PartnerCompany.objects.create(
        logo=image,
        url="https://example.com"
    )
    assert company.id is not None
    assert company.name is None  
    assert company.url == "https://example.com"
    assert company.is_active is True  


@pytest.mark.django_db
def test_create_partner_company_full():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")

    company = PartnerCompany.objects.create(
        logo=image,
        name="Test Company",
        url="https://testcompany.com",
        is_active=False
    )
    assert company.name == "Test Company"
    assert company.url == "https://testcompany.com"
    assert company.is_active is False


@pytest.mark.django_db
def test_str_method():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany.objects.create(
        logo=image,
        name="MyCompany",
        url="https://mycompany.com"
    )
    expected_str = "MyCompany https://mycompany.com"
    assert str(company) == expected_str


@pytest.mark.django_db
def test_name_can_be_blank_and_null():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany.objects.create(
        logo=image,
        name=None,
        url="https://blankname.com"
    )
    assert company.name is None

    company2 = PartnerCompany.objects.create(
        logo=image,
        name="",
        url="https://blankname2.com"
    )
    assert company2.name == ""


@pytest.mark.django_db
def test_url_field_must_be_valid():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany(
        logo=image,
        name="InvalidURL",
        url="not-a-valid-url"
    )
    with pytest.raises(ValidationError):
        company.full_clean()  


@pytest.mark.django_db
def test_is_active_default_true():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany.objects.create(
        logo=image,
        url="https://defaultactive.com"
    )
    assert company.is_active is True


@pytest.mark.django_db
def test_toggle_is_active():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany.objects.create(
        logo=image,
        url="https://toggleactive.com"
    )
    assert company.is_active is True
    company.is_active = False
    company.save()
    company.refresh_from_db()
    assert company.is_active is False


@pytest.mark.django_db
def test_logo_field_required():
    company = PartnerCompany(
        url="https://nologo.com"
    )
    with pytest.raises(ValidationError):
        company.full_clean()


@pytest.mark.django_db
def test_verbose_names():
    assert PartnerCompany._meta.verbose_name == "Partner company"
    assert PartnerCompany._meta.verbose_name_plural == "Partner companies"


@pytest.mark.django_db
def test_logo_upload_to_path():
    image = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    company = PartnerCompany.objects.create(
        logo=image,
        url="https://uploadpath.com"
    )
    assert company.logo.name.startswith("partners/logos/")
