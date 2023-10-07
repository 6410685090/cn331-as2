
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from register.models import Student ,Course
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
                return HttpResponseRedirect(reverse('signup'))
        student = Student.objects.get(user=request.user)
        return render(request, "register/index.html", {
                'student': student,
                'course': student.cstudent.all(),
                'add': Course.objects.filter(student=student).all(),
                'not_add': Course.objects.exclude(student=student).all(),
                'allcourse' : Course.objects.all,
            })
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect(reverse('signup'))
            student = Student.objects.get(user=user)
            return render(request, "register/index.html", {
                'student': student,
                'course': student.cstudent.all(),
                'add': Course.objects.filter(student=student).all(),
                'not_add': Course.objects.exclude(student=student).all(),
                'allcourse' : Course.objects.all,
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
            student = Student(user=user,name =fname,lastname=lname,student_id =username)
            student.save()
            user.save()
            return HttpResponseRedirect(reverse('signup'))
        else:
            return render(request, 'users/signup.html', {
        'message': 'Password not match.'
        })
    return render(request, "users/signup.html")

def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
    })

def changepassword(request):
    if request.method == "POST":
        if request.POST["newpass"] == request.POST["cnewpass"]:
            user = User.objects.get(username = request.user)
            user.set_password(request.POST["newpass"])
            user.save()
            logout_view(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'users/chpass.html',{
                'message' : 'Password not match.'
            })
    return render(request, 'users/chpass.html')