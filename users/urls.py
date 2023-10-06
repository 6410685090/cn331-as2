from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view,),
    path('index', views.index, name="user"),
    path('<str:courseid>/index',views.courseinfo,name='courseinfo'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup,name='signup'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('managecourse', views.mycourse, name='mycourse'),
    path('changepassword',views.changepassword,name='changepass')
]