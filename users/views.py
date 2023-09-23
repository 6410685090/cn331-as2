
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student , Course
# Create your views here.

def index(request):
    user = request.user
    student = Student.objects.get(user=user)
    return render(request, "users/index.html", {
        'student': student,
        'course': student.cstudent.all(),
        'add': Course.objects.filter(student=student).all(),
        'not_add': Course.objects.exclude(student=student).all()
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
                'course': student.cstudent.all(),
                'add': Course.objects.filter(student=student).all(),
                'not_add': Course.objects.exclude(student=student).all()
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
        'message': 'Confirm Password Incorrect'
        })
    return render(request, "users/signup.html")

def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
        
    })

def add(request):
    if request.method == "POST":
        course = Course.objects.get(subject_id = request.POST["course"])
        user = request.user
        if course.seat == 0:
            student = Student.objects.get(user=user)
            return render(request, "users/index.html",{
                'message': "There are no seats available",
                'student': student,
                'course': student.cstudent.all(),
                'add': Course.objects.filter(student=student).all(),
                'not_add': Course.objects.exclude(student=student).all(),
            })
        else:
            student = Student.objects.get(user=user)
            course.student.add(student)
            course.seat -= 1
            course.save()
            return HttpResponseRedirect(reverse('user'))
            
def remove(request):
    if request.method == "POST":
        user = request.user
        student = Student.objects.get(user=user)
        course = Course.objects.get(subject_id = request.POST["course"])
        course.student.remove(student)
        course.seat += 1
        course.save()
        return HttpResponseRedirect(reverse('user'))
    
