from django.shortcuts import get_object_or_404, render

from .models import Product

def home(request):
    return render(request, 'productsApp/home.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'productsApp/components/product_descr.html', {'product': product})
# Create your views here.
