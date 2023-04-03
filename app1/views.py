from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Contact
from .models import Product, Cart, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import razorpay
from datetime import date, timedelta,datetime




def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def aboutus(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        contact_model = Contact.objects.create(
            Name=request.POST.get('Cname'),
            Email=request.POST.get('Cemail'),
            Contact=request.POST.get('Ccontact'),
            Subject=request.POST.get('Csubject'),
            Message=request.POST.get('Cmessage')
        )
        messages.success(request, 'Your message has been successfully sent.')
        return render(request, 'contact.html')
    else:
        return render(request, 'contact.html')
    
    
    


def faqs(request):
    return render(request, 'FAQs.html')


def checkout(request):
    return render(request, 'checkout.html')


def bicyclelist(request):
    products = Product.objects.all()
    return render(request, 'bicyclelist.html', {'products': products})


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
        else:
            User.objects.create_user(uname, email, pass1)
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

    if not created:
        cart_item.quantity += 1
    if product.image:
        cart_item.image = product.image
    cart_item.price = product.product_price if product.product_price else 0
    cart_item.save()

    return redirect('cart')


@login_required(login_url='/accounts/login/')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False, defaults={'is_paid': False})
    cart_items = cart.cartitem_set.all()

    if request.method == 'POST':
        # Get start and end dates from the form
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Calculate the number of days between the start and end dates
        num_days = (end_date - start_date).days
        cart.num_days = num_days
        cart.start_date = start_date
        cart.end_date = end_date
        cart.save()
    else:
        # Use cart's current num_days value
        num_days = cart.num_days or 7  # default to 7 if num_days is not set
        today = datetime.today().date()
        start_date = today + timedelta(days=num_days)
        end_date = start_date + timedelta(days=7)

    total_price = sum(item.product.product_price * item.quantity for item in cart_items) * num_days
    total_price_security = total_price + 1000
    razor_amount = int(total_price_security) * 100

    context = {
        'items': cart_items,
        'total_price_security': total_price_security,
        'total_price': total_price,
        'razor_amount': razor_amount,
        'num_days': num_days,
    }

    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user, is_paid=False)

    cart_item, created = CartItem.objects.get_or_create(
        product=product, cart=cart)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # Save the product image and price to the cart item
    if product.image:
        cart_item.image = product.image
    # set default value for price
    cart_item.price = product.product_price if product.product_price else 0
    cart_item.save()

    return redirect('cart')





def clear_cart(request):
    CartItem.objects.filter(cart__user=request.user).delete()
    messages.success(request, 'Cart has been cleared successfully!')
    return redirect('cart')


def delete_from_cart(request, cart_item_id):
    get_object_or_404(CartItem, id=cart_item_id).delete()
    return redirect('cart')


def invoice(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Calculate total price
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)
    total_price = Decimal(total_price).quantize(Decimal('.01'))
    total_price_security = total_price + 1000

    context = {
        'total_price': total_price,
        'total_price_security': total_price_security,
        'items': cart_items,
    }

    return render(request, 'invoice.html', context)




def product_list(request):
    sort = request.GET.get('sort', None)
    products = Product.objects.all()

    if sort == 'availability_asc':
     products = products.order_by('product_quantity')
     print('Sorting by availability (low to high)')
    elif sort == 'availability_desc':
     products = products.order_by('-product_quantity')
     print('Sorting by availability (high to low)')
    elif sort == 'price_asc':
     products = products.order_by('product_price')
     print('Sorting by price (low to high)')
    elif sort == 'price_desc':
     products = products.order_by('-product_price')
     print('Sorting by price (high to low)')



    context = {'products': products}
    return render(request, 'bicyclelist.html', context)