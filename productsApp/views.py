from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm, ProfileUpdateForm
from .models import Cake



def home(request):
    
    cakes = Cake.objects.all()[:6]
    
    return render(request, 'productsApp/home.html', {'cakes': cakes})
  
def checkout(request):
  cakes = Cake.objects.all()[:1]
  return render(request, 'productsApp/checkout.html',{'cakes': cakes})
 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)  # Automatically log the user in after signup
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = SignupForm()
    return render(request, 'productsApp/signup.html', {'form': form})
    

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'productsApp/profile.html', {'form': form})
