from django.http import Http404, HttpResponse
# __init__.py
# Create your views here.
from django.shortcuts import get_object_or_404
from products.models import Product


product = get_object_or_404(Product, pk=1, slug="yar-menim")
"Selected Query doesnt match Product"

# try:
#     product = Product.objects.get(pk=1, slug="yar-menim")
# except Product.DoesNotExist:
    # product.rating -= 0.001
    # product.save()
    # send_sms("911", "hansisa user produkt axtardi tapmadi")
    # raise Http404("Selected Query doesnt match Product")