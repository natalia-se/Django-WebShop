from django.http import HttpResponse
from django.shortcuts import render
from .models import Cake


def home(request):
    
    cakes = Cake.objects.all()[:6]
    
    return render(request, 'productsApp/home.html', {'cakes': cakes})
  
def test_page(request):
  cakes = Cake.objects.all()[:1]
  return render(request, 'productsApp/checkout.html',{'cakes': cakes})
