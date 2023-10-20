from django.test import TestCase , Client
from .models import Student , Course
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
# Create your tests here.



class ViewTestCase(TestCase):

    def setUp(self):

        course2 = Course.objects.create(subject_id="1",subject="1"
                                        ,semester="1",year="1",seat="1",
                                        available=True)
        self.user1 = User.objects.create_user(username="123",password="123")
        self.admin = User.objects.create_superuser(username="admin",password="123")
        student = Student.objects.create(user=self.user1,
                                         student_id=self.user1.username)


    def test_client_login(self):
        """ If you can reach user page return 200"""
        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200) # Check login page
    
        logged_in = c.login(username=self.user1.username,password="123")
        self.assertTrue(logged_in) # Check login 

        response = c.post(reverse('user'))
        self.assertEqual(response.status_code, 200) # Check when login go to user

    def test_admin_login(self):
        """ If you can reach signup page return 200"""
        c = Client()    
        logged_in = c.login(username=self.admin.username,password="123")
        self.assertTrue(logged_in) # Check login 

        response = c.post(reverse('user'))
        self.assertRedirects(response, "/signup") # if admin user login will go to sign up page

    def test_courseinfo(self):
        """ If you can reach course info page return 200 """
        c = Client()
        c.login(username=self.user1.username,password="123")
        response = c.get(reverse('courseinfo', args=("1"))) # Course that have subject_id = 1
        self.assertEqual(response.status_code, 200) # Check course info

    def test_add_course(self):
        """ if add success return 302 """
        c = Client()
        c.login(username=self.user1.username,password="123")
        course = Course.objects.get(subject_id="1")
        data = {"course" : "1"}
        response = c.post(reverse("add"),data=data)
        self.assertEqual(response.status_code, 302) # Check add course
        self.assertTrue(course.student.count() == 1) # if add success student will incresses

    def test_remove_course(self):
        """ if remove success return 302 """
        c = Client()
        c.login(username=self.user1.username,password="123")
        course = Course.objects.get(subject_id="1")
        student = Student.objects.get(user=self.user1)
        course.student.add(student)
        course.save()
        data = {"course" : "1"}
        response = c.post(reverse("remove"),data=data)
        self.assertEqual(response.status_code, 302) # Check add course
        self.assertTrue(course.student.count() == 0) # if remove success student will decresses

    def test_mycourse_page(self):
        """ If you can reach mycourse page return 200 """
        c = Client()
        c.login(username=self.user1.username,password="123")
        response = c.post(reverse("mycourse"))
        self.assertEqual(response.status_code, 200) # If you can reach page return 200

    def test_logout(self):
        """ If you logout logged_in return False """
        c = Client()
        c.login(username=self.user1.username,password="123")
        logged_in = c.login(username=self.user1.username,password="123")
        self.assertTrue(logged_in) # Check login 
        logged_in = c.logout()
        self.assertFalse(logged_in) # Check logout

    def test_signup(self):
        """ Test sign up """
        c = Client()
        logged_in = c.login(username=self.admin.username,password="123") 
        self.assertTrue(logged_in) # Check login 
        
        response = c.post(reverse("user")) 
        self.assertEqual(response.status_code, 302) # can be reach
        data = {"username" : "james",
                "password" : "123",
                "cpassword" : "123",
                "email" : "Jedtapat@cn330.com",
                "fname" : "Jedtapat",
                "lname" : "Tanthiew",
                }
        response = c.post(reverse('signup'),data=data)
       
        c.logout()
        logged_in = c.login(username="james",password="123") 
        self.assertTrue(logged_in) # Check new user login 
     
    def test_changepass(self):
        """ Test sign up """
        c = Client()
        logged_in = c.login(username=self.user1.username,password="123") 
        self.assertTrue(logged_in) # Check login 

        data ={"newpass" : "555" , "cnewpass" : "555"}
        c.post(reverse('changepass'),data=data)

        c.logout()
        logged_in = c.login(username=self.user1.username,password="555") 
        self.assertTrue(logged_in) # Check new pass login 
