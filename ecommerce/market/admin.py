from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class Client_display(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain', 'address')


class Categories_display(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'status')


class Store_display(admin.ModelAdmin):
    list_display = ('id', 'address', 'post_code', 'business_email', 'business_name', 'business_address')


class Product_diaplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'slug', 'status')


class Attributes_display(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'product_id')


class WishList_display(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_id', 'init_price', 'created_date')


class Product_category_display(admin.ModelAdmin):
    list_display = ('id', 'category_id')


class Product_thumbnail_display(admin.ModelAdmin):
    list_display = ('id', 'name', 'thumbnail_url', 'product_variant_id')

class Order_display(admin.ModelAdmin):
    list_display = ('id', 'order_active_status', 'created_date', 'updated_date')

class Cart_display(admin.ModelAdmin):
    list_display = ('id', 'amount', 'initial_price', 'created_date')

class Vat_display(admin.ModelAdmin):
    list_display = ('id', 'vat_percentage', 'created_date','updated_date')

class Vat_Status_display(admin.ModelAdmin):
    list_display = ('id', 'amount', 'created_date','updated_date')

class Payment_method_display(admin.ModelAdmin):
    list_display = ('id', 'option', 'billing_address', 'security_code', 'country', 'minimum_amount', 'maximum_amount', 'method_status', 'currency',)

class Payment_status_display(admin.ModelAdmin):
    list_display = ('id', 'progress','charges', 'created_date', 'updated_date')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Client, Client_display)
admin.site.register(Stores, Store_display)
admin.site.register(Category, Categories_display)
admin.site.register(Products, Product_diaplay)
admin.site.register(Wish_list, WishList_display)
admin.site.register(Attributes, Attributes_display)
admin.site.register(Product_category, Product_category_display)
admin.site.register(Product_thumbnail, Product_thumbnail_display)
admin.site.register(Orders, Order_display)
admin.site.register(Cart, Cart_display)
admin.site.register(Vat, Vat_display)
admin.site.register(Vat_Status, Vat_Status_display)
admin.site.register(Payment_Method, Payment_method_display)
admin.site.register(Payment_Stauts, Payment_status_display)
admin.site.register(Shiping_Method)
admin.site.register(Shiping_Status)


