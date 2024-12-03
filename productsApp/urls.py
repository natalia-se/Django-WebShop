from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView

from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('signup/', views.signup, name='signup'), 
    path('login/', auth_views.LoginView.as_view(template_name='productsApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
    path('profile/', views.profile, name='profile'),  
	path('about/', views.about_us, name='about_us'), 
    path('password-change/', PasswordChangeView.as_view(template_name='productsApp/password-change.html', success_url='/profile/'), name='password_change'),  
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
	path('product/<int:product_id>/',views.product_detail,name='product_detail'),
    path('contact/', views.contact, name='contact'), 
    path('checkout/', views.place_order, name='checkout'),      
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
