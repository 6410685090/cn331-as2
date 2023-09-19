from django.db import models

# Create your models here.

class Course(models.Model):
    subject = models.CharField(max_length=64)
    subject_id = models.CharField(max_length=5)
    seat = models.IntegerField()

    def __str__(self):
        return f"{self.subject_id}: {self.seat} seatleft"

