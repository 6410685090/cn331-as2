from django.contrib import admin
from .models import Student , Course
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ["subject_id" , "subject", "available", "seat"]
    filter_horizontal = ["student"]


admin.site.register(Student)
admin.site.register(Course,CourseAdmin)