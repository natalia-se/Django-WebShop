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
    path('password-change/', PasswordChangeView.as_view(template_name='productsApp/password-change.html', success_url='/profile/'), name='password_change'),     
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
    path('product/<int:product_id>/',views.product_detail,name='product_detail'), 
    path('about/', views.about_us, name='about_us'),       
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
