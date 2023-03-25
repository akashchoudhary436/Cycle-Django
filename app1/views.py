from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def index(request):
    return render(request, 'index.html')


def aboutus(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def faqs(request):
    return render(request, 'FAQs.html')


def checkout(request):
    return render(request, 'checkout.html')


def bicyclelist(request):
    return render(request, 'bicyclelist.html')

def cart(request):
    return render(request, 'cart.html')



#sign up

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
           messages.error(request,'Your password and confirm password are not Same!!')
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')


# Login 

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')

    return render (request,'login.html')




#Logout

def LogoutPage(request):
    logout(request)
    return redirect('home')