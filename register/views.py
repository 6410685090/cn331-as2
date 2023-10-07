from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from register.models import Student , Course
# Create your views here.

def index(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
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

def mycourse(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if user.is_staff:
        return HttpResponseRedirect(reverse('signup'))
    student = Student.objects.get(user=user)
    return render(request, "register/mycourse.html",{
        'student': student,
        'course': student.cstudent.all(),
        'add': Course.objects.filter(student=student).all(),
        'not_add': Course.objects.exclude(student=student).all(),
        'allcourse' : Course.objects.all,
    })

def courseinfo(request,courseid):
    course = Course.objects.get(subject_id=courseid)
    return render(request, "register/info.html", {
        'course': course,
    })

def add(request):
    user = request.user
    student = Student.objects.get(user=user)
    if "course" in request.POST:       
        if request.method == "POST":
            course = Course.objects.get(subject_id = request.POST["course"])
            if course.seat == 0:
                return render(request, "register/mycourse.html",{
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
                course.save()
                return HttpResponseRedirect(reverse('mycourse'))
    else:
        return render(request, "register/mycourse.html",{
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
            course.seat += 1
            course.save()
            return HttpResponseRedirect(reverse('mycourse'))
    else:
        return render(request, "register/mycourse.html",{
                    'allcourse' : Course.objects.all,
                    'messageremove': "No course available",
                    'student': student,
                    'course': student.cstudent.all(),
                    'add': Course.objects.filter(student=student).all(),
                    'not_add': Course.objects.exclude(student=student).all(),
                })

