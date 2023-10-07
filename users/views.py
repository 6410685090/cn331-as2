
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student , Course
# Create your views here.

def index(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if user.is_staff:
        return HttpResponseRedirect(reverse('signup'))
    student = Student.objects.get(user=user)
    return render(request, "users/index.html", {
        'student': student,
        'course': student.cstudent.all(),
        'add': Course.objects.filter(student=student).all(),
        'not_add': Course.objects.exclude(student=student).all(),
        'allcourse' : Course.objects.all,
    })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user'))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect(reverse('signup'))
            student = Student.objects.get(user=user)
            return HttpResponseRedirect(reverse('user'))
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

def add(request):
    user = request.user
    student = Student.objects.get(user=user)
    if "course" in request.POST:       
        if request.method == "POST":
            course = Course.objects.get(subject_id = request.POST["course"])
            if course.seat == 0:
                return render(request, "users/mycourse.html",{
                    'allcourse' : Course.objects.all,
                    'message': "There are no seats available",
                    'student': student,
                    'course': student.cstudent.all(),
                    'add': Course.objects.filter(student=student).all(),
                    'not_add': Course.objects.exclude(student=student).all(),
                })
            else:
                course.student.add(student)
                course.seat -= 1
                if course.seat == 0:
                    course.available = False
                course.save()
                return HttpResponseRedirect(reverse('mycourse'))
    else:
        return render(request, "users/mycourse.html",{
                    'allcourse' : Course.objects.all,
                    'messageadd': "No course available",
                    'student': student,
                    'course': student.cstudent.all(),
                    'add': Course.objects.filter(student=student).all(),
                    'not_add': Course.objects.exclude(student=student).all(),
                })
    
def remove(request):
    user = request.user
    student = Student.objects.get(user=user)
    if "course" in request.POST:
        if request.method == "POST":
            course = Course.objects.get(subject_id = request.POST["course"])
            course.student.remove(student)
            if course.seat == 0:
                course.available = True
            course.seat += 1
            course.save()
            return HttpResponseRedirect(reverse('mycourse'))
    else:
        return render(request, "users/mycourse.html",{
                    'allcourse' : Course.objects.all,
                    'messageremove': "No course available",
                    'student': student,
                    'course': student.cstudent.all(),
                    'add': Course.objects.filter(student=student).all(),
                    'not_add': Course.objects.exclude(student=student).all(),
                })

def courseinfo(request,courseid):
    course = Course.objects.get(subject_id=courseid)
    return render(request, "users/info.html", {
        'course': course,
    })

def mycourse(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if user.is_staff:
        return HttpResponseRedirect(reverse('signup'))
    student = Student.objects.get(user=user)
    return render(request, "users/mycourse.html",{
        'student': student,
        'course': student.cstudent.all(),
        'add': Course.objects.filter(student=student).all(),
        'not_add': Course.objects.exclude(student=student).all(),
        'allcourse' : Course.objects.all,
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