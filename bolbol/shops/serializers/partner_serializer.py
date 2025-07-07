from rest_framework import serializers

from shops.models import PartnerCompany


class PartnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerCompany
        fields = "__all__"