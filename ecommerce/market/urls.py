from . import views
from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("allproducts/",views.allproducts),
    path("allclients/",views.allclients),
    # path('addclient/',views.addclient),
    path('categories',views.view_category),
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
]