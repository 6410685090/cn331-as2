from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage,name="mainpageuser"),
    path('index', views.index, name="indexuser"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register,name='register'),
]