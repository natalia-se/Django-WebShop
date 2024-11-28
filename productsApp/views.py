from django.http import HttpResponse
from django.shortcuts import render
from .models import Cake


from .models import Product

def home(request):
    
    cakes = Cake.objects.all()[:6]
    
    return render(request, 'productsApp/home.html', {'cakes': cakes})
  # return render(request, 'productsApp/components/products_list.html', {'cakes': cakes})
    return render(request, 'productsApp/home.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'productsApp/components/product_descr.html', {'product': product})
# Create your views here.
