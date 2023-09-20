from django.db import models

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

