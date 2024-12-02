from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .forms import SignupForm, ProfileUpdateForm
from .models import Cake, Cart, CartItem


def home(request):
    
    cakes = Cake.objects.all()[:6]
    
    return render(request, 'productsApp/home.html', {'cakes': cakes})

def product_detail(request, product_id):
    product = get_object_or_404(Cake, id=product_id)
    return render(request, 'productsApp/components/product_descr.html', {'product': product})
 
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
    return render(request, 'productsApp/signup.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Cake, id=product_id)
    return render(request, 'productsApp/components/product_descr.html', {'product': product})

def about_us(request):
   
    return render(request,'productsApp/components/about_us.html')

    

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

def add_to_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    
    if request.user.is_authenticated:
        # User is logged in, use the database cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    else:
        # User is not logged in, use the session cart
        cart = request.session.get('cart', {})
        if str(cake.id) in cart:
            cart[str(cake.id)]['quantity'] += 1
        else:
            cart[str(cake.id)] = {
                'name': cake.name,
                'price': str(cake.price),  # Convert Decimal to str for JSON serialization
                'quantity': 1,
                'image_url': cake.image.url if cake.image else '',
            }
        request.session['cart'] = cart
    
    return redirect('cart_detail')

def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        total = sum(item.total_price for item in items)
    else:
        cart = request.session.get('cart', {})
        items = [{'name': item['name'], 'price': item['price'], 'quantity': item['quantity']} for item in cart.values()]
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    return render(request, 'productsApp/cart.html', {'items': items, 'total': total})

def remove_from_cart(request, cart_item_id=None):
    if request.user.is_authenticated:
        # Handle removal for logged-in users
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user == request.user:
            cart_item.delete()
    else:
        # Handle removal for session-based carts
        cart = request.session.get('cart', {})
        if str(cart_item_id) in cart:
            del cart[str(cart_item_id)]
            request.session['cart'] = cart  # Update session cart

    return redirect('cart_detail')

@receiver(user_logged_in)
def merge_carts(sender, request, user, **kwargs):
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
    
    # Get or create the user's database cart
    cart, created = Cart.objects.get_or_create(user=user)
    for cake_id, item in session_cart.items():
        cake = Cake.objects.get(id=cake_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)
        if not created:
            cart_item.quantity += item['quantity']
        cart_item.save()
    
    # Clear the session cart
    request.session['cart'] = {}
