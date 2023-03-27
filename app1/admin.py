from django.contrib import admin
from .models import Product, Cart, CartItem

# Register your models here.
admin.site.register(Product)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
