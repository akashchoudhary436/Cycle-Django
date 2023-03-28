from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('aboutus/', views.aboutus, name='about'),
    path('bicyclelist/', views.bicyclelist, name='bicyclelist'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('invoice/', views.invoice, name='inovice'),
     path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
