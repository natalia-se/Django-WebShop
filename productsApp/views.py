from django.http import HttpResponse
from django.shortcuts import render
from .models import Cake


def home(request):
    
    cakes = Cake.objects.all()[:6]
    
    return render(request, 'productsApp/home.html', {'cakes': cakes})
  # return render(request, 'productsApp/components/products_list.html', {'cakes': cakes})
