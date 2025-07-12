from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from shops.documents import ShopDocument
from elasticsearch_dsl import Q


class ShopFilterAPIView(APIView):
    """
    Filter shops by activity and sort order.

    Supported query parameters:
    - activities: list of activity names (e.g., ?activities=Cleaning&activities=Delivery)
    - sort: one of ['name_asc', 'name_desc', 'product_count_desc', 'random']
    """
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request):
        sort = request.GET.get("sort")
        activities = request.GET.getlist("activities") 

        search = ShopDocument.search()

        if activities:
            nested_query = Q(
                "nested", 
                path="activities", 
                query=Q("terms", **{"activities.name.keyword": activities}))
            search = search.filter(nested_query)

        if sort == "name_asc":
            search = search.sort('name.raw')
        elif sort == "name_desc":
            search = search.sort('-name.raw')
        elif sort == "product_count_desc":
            search = search.sort('-product_count')
        elif sort == "random":
            search = search.sort({
                "_script": {
                    "type": "number",
                    "script": "Math.random()",
                    "order": "asc"
                }
            })
        else:
            search = search.sort('name.raw') 
        response = search.execute()

        results = []
        for hit in response:
            results.append({
                "id": hit.id,
                "name": hit.name,
                "product_count": hit.product_count,
            })
        return Response(results, status=status.HTTP_200_OK)