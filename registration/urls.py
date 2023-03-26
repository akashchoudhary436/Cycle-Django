
from django.contrib import admin
from django.urls import path
from app1 import views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
     path('contact/', views.contact, name='contact'),
    path('faqs/',views.faqs,name='faqs'),
    path('aboutus/',views.aboutus,name='about'),
    path('bicyclelist/',views.bicyclelist,name='bicyclelist'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/',views.cart,name='cart'),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('invoice/',views.invoice,name='inovice'),

  
    
]
