
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student
# Create your views here.

def index(request):
    return render(request, "users/index.html", {
        
    })

def mainpage(request):
    return render(request, "users/mainpage.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            student = Student.objects.get(user=user)
            login(request, user)
            return render(request, 'users/index.html', {
                'student': student,
                'user' : user
            })
        else:
            return render(request, 'users/login.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'users/login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        if password == cpassword:
            user = User.objects.create_user(username=username,
                email=email,password=password)
            user.first_name = fname
            user.last_name = lname
            student = Student(user=user)
            student.save()
            user.save()
            return HttpResponseRedirect(reverse('signup'))
        else:
            return render(request, 'users/signup.html', {
        'message': 'Confirm Password Incorrect'
        })
    return render(request, "users/signup.html")

def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
    })

