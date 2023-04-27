from . import views
from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("allproducts/",views.all_products),
    path("allclients/",views.all_clients),
    # path('addclient/',views.addclient),
    path('pricing/<int:id>',views.product_pricing),
    path('categories',views.view_category),
    path('register/', views.register, name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('product_thumbnail/<int:id>',views.product_thumbnail),
    path('store/<int:id>',views.store_info),
    path('add_wishlist/<int:id>',views.add_wishlist),
    
]