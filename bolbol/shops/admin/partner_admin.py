from django.contrib import admin
from shops.models import PartnerCompany


@admin.register(PartnerCompany)
class PartnerCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "url")
