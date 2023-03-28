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

# View function for rendering index page


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html')


# View function for rendering about page
def aboutus(request):
    return render(request, 'about.html')


# View function for rendering contact page and processing form submission
def contact(request):
    if request.method == 'POST':

        # Get values from form submission
        Name = request.POST.get('Cname')
        Email = request.POST.get('Cemail')
        contact_val = request.POST.get('Ccontact')
        Subject = request.POST.get('Csubject')
        Message = request.POST.get('Cmessage')

        # Print form values to console
        print(Name, Email, contact_val, Subject, Message)

        # Add success message for successful form submission
        messages.success(request, 'Your message has Successfully Sent')

        # Save contact details to Contact model
        contact_model = Contact(
            Name=Name, Email=Email, Contact=contact_val, Subject=Subject, Message=Message)
        contact_model.save()

        return render(request, 'contact.html')
    else:

        # Render contact page if request method is not POST
        return render(request, 'contact.html')


# View function for rendering FAQs page
def faqs(request):
    return render(request, 'FAQs.html')


# View function for rendering checkout page
def checkout(request):
    return render(request, 'checkout.html')


# View function for rendering invoice page


# View function for rendering bicycle list page
def bicyclelist(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'bicyclelist.html', context)


# View function for rendering cart page
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    context = {'items': cart_items}
    return render(request, 'cart.html', context)


# View function for rendering signup page and processing form submission
def SignupPage(request):
    if request.method == 'POST':

        # Get values from form submission
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(
                request, 'Your password and confirm password are not Same!!')
        else:

            # Create new user and redirect to login page if passwords match
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')


# View function for rendering login page and processing form submission
def LoginPage(request):
    if request.method == 'POST':

        # Get values from form submission
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        # Authenticate user and redirect to home page
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:

            # Add error message for invalid credentials
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login.html')

# View function for logging out user and redirecting to home page


def LogoutPage(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

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


def invoice(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Calculate total price
    total_price = sum(item.product.product_price *
                      item.quantity for item in cart_items)
    total_price = Decimal(total_price).quantize(Decimal('.01'))
    total_price_security = calculate_total_price(cart_items) + 1000
    context = {
        'total_price': total_price,
        'total_price_security': total_price_security,
        'items': cart_items,
    }

    return render(request, 'invoice.html', context)


def calculate_total_price(cart_items):
    total_price = sum(item.product.product_price *
                      item.quantity for item in cart_items)
    total_price = Decimal(total_price).quantize(Decimal('.01'))
    return total_price


def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = calculate_total_price(cart_items)
    total_price_security = calculate_total_price(cart_items) + 1000
    context = {
        'items': cart_items,
        'total_price_security': total_price_security,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)





def clear_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    cart_items.delete()
    messages.success(request, 'Cart has been cleared successfully!')
    return redirect('cart')




def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
