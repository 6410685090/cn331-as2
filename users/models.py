from django.db import models
from django.contrib.auth.models import User
# Create your models here.
   
class Student(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=64,default="-")
    lastname = models.CharField(max_length=64,default="-")
    student_id = models.CharField(max_length=10,default="-")

    def __str__(self):
        return f"{self.name} {self.lastname}"
    
class Course(models.Model):
    subject = models.CharField(max_length=64)
    subject_id = models.CharField(max_length=5)
    semester = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    seat = models.IntegerField()
    available = models.BooleanField(default=True)
    student = models.ManyToManyField(Student, blank=True, related_name="cstudent")

    def __str__(self):
        return f"{self.subject_id} : {self.seat} Seatleft"
    