from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, "users/index.html")

def mainpage(request):
    return render(request, "users/mainpage.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('indexuser'))
        else:
            return render(request, 'users/login.html', {
                'message': 'Invalid credentials.'
            })

    return render(request, "users/login.html")

def mainpage(request):
    return render(request, "users/mainpage.html")
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        email = request.POST['email']
        if password == cpassword:
            user = User.objects.create_user(username=username,
                email=email,password=password)
            user.save()
            return render(request, "users/login.html")
        else:
            return render(request, 'users/register.html', {
        'message': 'Confirm Password incorrect'
        })
    return render(request, "users/register.html")

def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
    })


