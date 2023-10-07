from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name="user"),
    path('info/<str:courseid>',views.courseinfo,name='courseinfo'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('managecourse', views.mycourse, name='mycourse'),
]