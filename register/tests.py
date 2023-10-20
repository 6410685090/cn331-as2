from django.test import TestCase
from .models import Student , Course
from django.contrib.auth.models import User

# Create your tests here.



class RegisterTestCase(TestCase):

    def setUp(self):

        course1 = Course.objects.create(subject_id="1",subject="1"
                                        ,semester="1",year="1",seat="1",
                                        available=True)
        self.user1 = User.objects.create_user(username="123",password="123")
        student = Student.objects.create(user=self.user1,student_id=self.user1.username)


    def test_seat_available(self):
        """ seat available"""
        course = Course.objects.get(subject_id="1")
        course.seat = 1
        course.save()
        self.assertTrue(course.seat>0)

    
    def test_seat_not_available(self):
        """ seat not available """
        course = Course.objects.get(subject_id="1")
        course.seat = 0
        course.save()
        self.assertTrue(course.seat<=0)


    def test_available_status(self):
        """ Course Available """
        course = Course.objects.get(subject_id="1")
        self.assertTrue(course.available)

    def test_not_available_status(self):
        """ Course Available """
        course = Course.objects.get(subject_id="1")
        course.available = False
        course.save()
        self.assertFalse(course.available)