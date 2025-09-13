from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from shops.serializers import PartnerCompanySerializer
from shops.models import PartnerCompany
from drf_yasg.utils import swagger_auto_schema

__all__ = ("PartnerCompanyListAPIView",)


class PartnerCompanyListAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_summary="List Active Partner Companies",
        operation_description="Returns a list of all active partner companies.",
        responses={200: PartnerCompanySerializer(many=True)}
    )
    def get(self, request):
        partner_companies = PartnerCompany.objects.filter(is_active=True)
        serializer = PartnerCompanySerializer(partner_companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



