from django.db import models
from django.contrib.auth.models import User
# Create your models here.
   
class Course(models.Model):
    subject = models.CharField(max_length=64)
    subject_id = models.CharField(max_length=5)
    semester = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    seat = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_id}: {self.seat} seatleft"

class Student(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True, related_name="student")

    def name(self):
        return f"{self.user.first_name}"
    def lastname(self):
        return f"{self.user.last_name}"
    def studentid(self):
        return f"{self.user.username}"
    def __str__(self):
        return f"{self.user.first_name}: {self.user.last_name}"