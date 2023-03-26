from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Contact


# View function for rendering index page
def index(request):
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
        contact_model = Contact(Name=Name, Email=Email, Contact=contact_val, Subject=Subject, Message=Message)
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
def invoice(request):
    return render(request, 'invoice.html')


# View function for rendering bicycle list page
def bicyclelist(request):
    return render(request, 'bicyclelist.html')


# View function for rendering cart page
def cart(request):
    return render(request, 'cart.html')


# View function for rendering signup page and processing form submission
def SignupPage(request):
    if request.method=='POST':
        
        
        # Get values from form submission
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')


        # Check if passwords match
        if pass1 != pass2:
            messages.error(request,'Your password and confirm password are not Same!!')
        else:
            
            
            # Create new user and redirect to login page if passwords match
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')


# View function for rendering login page and processing form submission
def LoginPage(request):
    if request.method=='POST':
        
        # Get values from form submission
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        
        
        # Authenticate user and redirect to home page
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request,'Successfully logged in')
            return redirect('home')
        else:
            
            # Add error message for invalid credentials
            messages.error(request,'Invalid Credentials')

    return render(request,'login.html')

# View function for logging out user and redirecting to home page
def LogoutPage(request):
    logout(request)
    return redirect('home')
