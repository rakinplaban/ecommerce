from . import views

from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("allproducts/",views.allproducts),
    path("allclients/",views.allclients),
    path('addclient/',views.addclient),
    path('register/', views.register, name='register'),
]