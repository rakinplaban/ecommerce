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
    path('wishlist',views.view_wishlist),
    path('remove_wishlist/<int:id>',views.remove_from_wishlist),
    path('add_to_cart/<int:id>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('update_cart/<int:id>',views.update_cart),
    path('remove_cart/<int:id>',views.delete_cart_item),
    path('create_order',views.create_order),
    path('track_order',views.track_orders),
]