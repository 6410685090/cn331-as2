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
        """ If you can reach user page """
        c = Client()

        response = c.get(reverse('user'))
        self.assertRedirects(response, "/login") # if not login will return to login page

        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200) # Check login page
        
        data = {"username" : "123" , "password" : "123"}
        response = c.post(reverse('login'),data=data)
        response = c.get(reverse('user'))
        self.assertEqual(response.status_code, 200) # Check when login go to user
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200) # Check when login go to user

        c.logout()
        data = {"username" : "12345" , "password" : "123321"} # fake user
        response = c.post(reverse('login'),data=data)
        self.assertEqual(response.status_code, 200) # return to login page

    def test_admin_login(self):
        """ If you can reach signup page """
        c = Client()    
        data = {"username" : "admin" , "password" : "123"}
        response = c.post(reverse('login'),data=data)
        self.assertEqual(response.status_code, 302) # Check when login 

        response = c.post(reverse('login'))
        self.assertRedirects(response, "/signup") # if admin user login will go to sign up page

        response = c.post(reverse('user'))
        self.assertRedirects(response, "/signup") # if admin user login will go to sign up page

    def test_courseinfo(self):
        """ If you can reach course info page """
        c = Client()
        c.login(username=self.user1.username,password="123")
        response = c.get(reverse('courseinfo', args=("1"))) # Course that have subject_id = 1
        self.assertEqual(response.status_code, 200) # Check course info

    def test_add_course(self):
        """ if add success """
        c = Client()
        c.login(username=self.user1.username,password="123")
        course = Course.objects.get(subject_id="1")
        data = {"course" : "1"}
        response = c.post(reverse("add"),data=data)
        self.assertTrue(course.student.count() == 1) # if add success student will incresses
        
        course.student.remove(Student.objects.get(user=self.user1))
        course.seat = 0
        course.save()
        response = c.post(reverse("add"),data=data)
        self.assertEqual(response.status_code, 200)  
        self.assertTrue(course.student.count() == 0) # if add when seat full student won't incresses

        c.get(reverse("add")) 
        self.assertEqual(response.status_code, 200) 
        self.assertTrue(course.student.count() == 0) # if add when method is get student won't incresses

    def test_remove_course(self):
        """ if remove success """
        c = Client()
        c.login(username=self.user1.username,password="123")
        course = Course.objects.get(subject_id="1")
        student = Student.objects.get(user=self.user1)
        course.student.add(student)
        course.save()
        data = {"course" : "1"}
        response = c.post(reverse("remove"),data=data)
        self.assertEqual(response.status_code, 302) # Check remove course
        self.assertTrue(course.student.count() == 0) # if remove success student will decresses

        course.student.add(student)
        course.save()
        c.get(reverse("remove")) 
        self.assertRedirects(response, "/user/managecourse") # if method is not post will return to /managecourse
        self.assertTrue(course.student.count() == 1) # if remove when method is get student won't decresses

    def test_mycourse_page(self):
        """ If you can reach mycourse page """
        c = Client()
        c.login(username=self.user1.username,password="123")
        response = c.get(reverse("mycourse"))
        self.assertEqual(response.status_code, 200) # If sucess will reach to /user/managecourse and return 200
        c.logout()
        response = c.get(reverse("mycourse"))
        self.assertRedirects(response, "/login") # If not login will return to login page
        c.login(username="admin",password="123")
        response = c.get(reverse("mycourse"))
        self.assertRedirects(response, "/signup") # If login as admin will return to signup page

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

        data = {"username" : "james",
                "password" : "123",
                "cpassword" : "123",
                "email" : "Jedtapat@cn331.com",
                "fname" : "Jedtapat",
                "lname" : "Tanthiew",
                }
        response = c.post(reverse('signup'),data=data)

        c.logout()
        logged_in = c.login(username="james",password="123") 
        self.assertTrue(logged_in) # Check new user login 
        c.logout()
        logged_in = c.login(username=self.admin.username,password="123") 
        self.assertTrue(logged_in) # Check login 

        data = {"username" : "net",
                "password" : "123",
                "cpassword" : "555",
                "email" : "Chanyanuch@cn331.com",
                "fname" : "Chanyanuch",
                "lname" : "Jumnongit",
                }
        
        response = c.post(reverse('signup'),data=data) # if password != comfirm password
        c.logout()
        logged_in = c.login(username="net",password="123") 
        self.assertFalse(logged_in) # Check new user can't login because it not create yet

    def test_changepass(self):
        """ Test change password """
        c = Client()
        logged_in = c.login(username=self.user1.username,password="123") 
        self.assertTrue(logged_in) # Check login 

        data ={"newpass" : "555" , "cnewpass" : "555"}
        c.post(reverse('changepass'),data=data)
        c.logout()
        logged_in = c.login(username=self.user1.username,password="555") 
        self.assertTrue(logged_in) # Check new pass login 

        data ={"newpass" : "333" , "cnewpass" : "332"}
        c.post(reverse('changepass'),data=data)
        c.logout()
        logged_in = c.login(username=self.user1.username,password="333") 
        self.assertFalse(logged_in) # Check new pass can't login because it not change yet

        logged_in = c.login(username=self.user1.username,password="555") 
        self.assertTrue(logged_in) # Check new pass login 
        response = c.get(reverse('changepass'))
        self.assertTrue(response.status_code == 200) # if method is get will return 200

