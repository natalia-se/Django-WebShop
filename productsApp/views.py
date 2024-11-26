from django.shortcuts import render

def home(request):
    return render(request, 'productsApp/home.html')

# Create your views here.
def index(request):
    return render(request,'productsApp/components/homepage.html')