from django.shortcuts import render

from .models import Course

# Create your views here.

def index(request):
    return render(request, "quota/index.html" , {
        'cs' : Course.objects.all()
        })

def info(request, id):
    course = Course.objects.get(pk=id)
    return render(request, "quota/course.html", {
        'course': course,
    })