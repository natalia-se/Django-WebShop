from django.contrib import admin

from .models import Cake, Contact, Order, OrderItem, Cart, CartItem

class CakeAdmin(admin.ModelAdmin):
    # Add 'id' to the list of fields displayed in the admin list view
    list_display = ('id', 'name', 'price', 'description', 'created_at')
    # Add 'id' to the fields you can search or filter by if desired
    search_fields = ('id', 'name')
    list_filter = ('created_at',)

admin.site.register(Cake, CakeAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'subject', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  # Fields to display in the list view
    search_fields = ('user__username',)  # Allow searching by username
    list_filter = ('created_at',)  # Add filters for the created date

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'cake', 'quantity', 'total_price')  # Fields to display
    search_fields = ('cart__user__username', 'cake__name')  # Allow searching by cart user or cake name
    list_filter = ('cart', 'cake')  # Add filters for cart and cake
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Disable extra empty rows

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'city', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at', 'shipping_method')
    search_fields = ('first_name', 'last_name', 'email', 'user__username', 'city', 'country')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
