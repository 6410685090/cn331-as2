from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage, name="main"),
    path('index', views.index, name="indexq"),
    path('<int:id>' , views.info, name="info")
]