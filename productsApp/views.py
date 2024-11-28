from django.http import HttpResponse
from django.shortcuts import render
from .models import Cake


def home(request):
    
    cake1 = Cake.objects.get(id=12) 
    cake2 = Cake.objects.get(id=11)
    cake3 = Cake.objects.get(id=10)
    cake4 = Cake.objects.get(id=9)
    cake5 = Cake.objects.get(id=8)
    cake6 = Cake.objects.get(id=7)
    
    return render(request, 'productsApp/home.html', {
  #  return render(request, 'productsApp/components/products_list.html', {
        'cake1': cake1,
        'cake2': cake2,
        'cake3': cake3,
        'cake4': cake4,
        'cake5': cake5,
        'cake6': cake6,
    })


""" def test_page(request):
   
    cake1 = Cake.objects.get(id=12) 
    cake2 = Cake.objects.get(id=11)
    cake3 = Cake.objects.get(id=10)
    cake4 = Cake.objects.get(id=9)
    cake5 = Cake.objects.get(id=8)
    cake6 = Cake.objects.get(id=7)
    
    return render(request, 'productsApp/components/products_list.html', {
        'cake1': cake1,
        'cake2': cake2,
        'cake3': cake3,
        'cake4': cake4,
        'cake5': cake5,
        'cake6': cake6,
    }) """
