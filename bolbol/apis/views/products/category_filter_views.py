from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from products.models import Category, CategoryFilterField
from products.serializers import CategorySerializer, SubcategorySerializer
from utils.constants import TimeIntervals

__all__ = (
    "SubcategoryAPIView",
    "SubcategoryFilterSchemaAPIView"
)


class SubcategoryAPIView(APIView):
    def get(self, request, category_pk, *args, **kwargs):
        categories = Category.objects.filter(parent_category__pk=category_pk, is_active=True)
        serializer = SubcategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


filter_data = {
    "Nəqliyyat": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Daşınmaz əmlak": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Geyim": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Uşaq aləmi": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Kosmetika və sağlamlıq": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "İş elanları": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Elektronika": {
        "isParentCategory": True,
        "subcategories": {
            "Telefonlar": {
                "autoGenerateProductName": True,
                "isSubcategory": True,
                "defaultFilters": {
                    "showPrice": True,
                    "showIsNew": True,
                    "showIsDeliveryAvailable": True,
                    "showIsBarterAvailable": True,
                    "showIsCreditAvailable": True,
                    "showIsViaNegotiator": True
                },
                "filters": [
                    {
                        "id": "brand",
                        "name": "Marka",
                        "type": "select",
                        "useForProductName": True,
                        "options": [
                            {
                                "id": "acer",
                                "name": "Acer",
                                "childFilters": [
                                    {
                                        "id": "model",
                                        "name": "Model",
                                        "type": "select",
                                        "useForProductName": True,
                                        "options": [
                                            {
                                                "id": "dx650",
                                                "name": "DX650",
                                                "childFilters": [
                                                    {
                                                        "id": "color",
                                                        "name": "Reng",
                                                        "type": "select",
                                                        "useForProductName": True,
                                                        "options": [
                                                            {
                                                                "id": "black",
                                                                "name": "black"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            },
                                            {
                                                "id": "predator8",
                                                "name": "Predator 8",
                                                "childFilters": [
                                                    {
                                                        "id": "color",
                                                        "name": "Reng",
                                                        "type": "select",
                                                        "useForProductName": True,
                                                        "options": [
                                                            {
                                                                "id": "black",
                                                                "name": "black"
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "id": "memory",
                                                        "name": "Yaddas",
                                                        "type": "select",
                                                        "useForProductName": True,
                                                        "options": [
                                                            {
                                                                "id": "32gb_2gb",
                                                                "name": "32gb/2gb"
                                                            },
                                                            {
                                                                "id": "64gb_2gb",
                                                                "name": "64gb/2gb"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": "accessories",
                                "name": "Aksesuarlar"
                            },
                            {
                                "id": "oppo",
                                "name": "OPPO"
                            },
                            {
                                "id": "aiek",
                                "name": "Aiek"
                            }
                        ]
                    }
                ]
            },
            "AnotherSubcategory": {}
        }
    },
    "Ev və Bağ üçün": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Ərzaq": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Heyvan, Bitki": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "İdman, musiqi, hobbi": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Digər": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Xidmətlər": {
        "isParentCategory": True,
        "subcategories": {}
    },
    "Pulsuz": {
        "isParentCategory": True,
        "subcategories": {}
    }
}


@method_decorator(cache_page(TimeIntervals.ONE_MIN_IN_SEC), name="dispatch")
class SubcategoryFilterSchemaAPIView(APIView):
    def get(self, request, category_pk, subcategory_pk, *args, **kwargs):
        parent_category = Category.objects.get(pk=category_pk, is_active=True)
        subcategory = Category.objects.get(pk=subcategory_pk, is_active=True)
        parent_name = parent_category.name
        sub_name = subcategory.name
        filter_schema = filter_data.get("Elektronika", {}).get("subcategories", {}).get("Telefonlar", {})
        return Response(filter_schema, status=status.HTTP_200_OK)