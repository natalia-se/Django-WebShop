from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    
  return render(request, 'productsApp/components/products_list.html')