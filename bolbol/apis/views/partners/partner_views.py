from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
# from shops.serializers import PartnerCompanySerializer
from shops.models import PartnerCompany

__all__ = ("PartnerCompanyListAPIView",)


class PartnerCompanyListAPIView(APIView):
    http_method_names = ["get"]

    def get(self, request):
        partner_companies = PartnerCompany.objects.filter(is_active=True)
        # serializer = PartnerCompanySerializer(partner_companies, many=True)
        serializer = None
        return Response(serializer.data, status=status.HTTP_200_OK)


from apis.views.shops.shop_views import * # all