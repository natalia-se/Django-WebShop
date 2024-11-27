from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'productsApp/home.html')

# Create your views here.

@login_required
def profile(request):
    return render(request, 'productsApp/profile.html')