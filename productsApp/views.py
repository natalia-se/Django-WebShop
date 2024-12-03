
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .forms import SignupForm, ProfileUpdateForm, ContactForm
from .models import Cake, Cart, CartItem, Contact, Order, OrderItem


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
                'cake_id': cake.id,
                'name': cake.name,
                'price': str(cake.price),  # Convert Decimal to str for JSON serialization
                'quantity': 1,
                'image_url': cake.image.url if cake.image else '',
            }
        request.session['cart'] = cart
    
    return redirect('cart_detail')

def cart_detail(request):
    if request.user.is_authenticated:
        # For authenticated users, fetch the cart and include item id
        cart = Cart.objects.filter(user=request.user).first()
        items = []
        if cart:
            for item in cart.items.all():
                items.append({
                    'id': item.id,  # Add the CartItem id
                    'cake_id': item.cake.id,
                    'name': item.cake.name,
                    'price': item.cake.price,
                    'quantity': item.quantity,
                    'total_price': item.total_price,
                    'image_url': item.cake.image.url if item.cake.image else None,  # Include the image URL
                })
        total = sum(item['total_price'] for item in items)
    else:
        # For non-authenticated users (session-based cart), use unique session ids
        cart = request.session.get('cart', {})
        items = []
        for cart_item_id, item in cart.items():
            total_price = float(item['price']) * item['quantity']
            items.append({
                'id': cart_item_id,  # Use the cart_item_id as a unique identifier for session-based carts
                'cake_id': item['cake_id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity'],
                'total_price': total_price,
                'image_url': item['image_url'] if 'image_url' in item else None,  # Include image URL if available
            })
        total = sum(item['total_price'] for item in items)

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

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                category=form.cleaned_data['category'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent. We will contact you soon!')
            return render(request, 'productsApp/contact.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    
    return render(request, 'productsApp/contact.html', {'form': form})

def place_order(request):
    if request.method == 'POST':
        # Collect order details from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')
        country = request.POST.get('country')
        shipping_method = request.POST.get('shipping_method')
        shipping_notes = request.POST.get('shipping_notes')

        if request.user.is_authenticated:
            # Fetch items from the user's database-backed cart
            cart = Cart.objects.filter(user=request.user).first()
            items = cart.items.all() if cart else []
        else:
            # Fetch items from the session cart
            session_cart = request.session.get('cart', {})
            items = [{
                'cake': Cake.objects.get(id=cake_id),
                'quantity': item['quantity']
            } for cake_id, item in session_cart.items()]

        # Ensure the cart is not empty
        if not items:
            return redirect('cart_detail')  # Redirect to cart if it's empty

        # Create the Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            city=city,
            postal_code=postal_code,
            province=province,
            country=country,
            shipping_method=shipping_method,
            shipping_notes=shipping_notes,
        )

        # Add Order Items
        cart_items = []
        total = 0
        for item in items:
            if request.user.is_authenticated:
                # `item` is a CartItem object
                cake = item.cake
                quantity = item.quantity
            else:
                # `item` is a dictionary for session-based cart
                cake = item['cake']
                quantity = item['quantity']

            total_price = cake.price * quantity
            OrderItem.objects.create(order=order, cake=cake, quantity=quantity)
            
            # Prepare cart_items for the template
            cart_items.append({
                'cake': cake,
                'quantity': quantity,
                'total_price': total_price,
            })
            total += total_price

        # Clear the cart
        if request.user.is_authenticated:
            cart.items.all().delete()
        else:
            request.session['cart'] = {}

        # Pass order details to the success page
        return render(request, 'productsApp/order_success.html', {
            'order': order,
            'cart_items': cart_items,
            'total': total,
        })

    return render(request, 'productsApp/checkout.html')
