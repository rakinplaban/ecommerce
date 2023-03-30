from django.contrib import admin
from .models import (Client,UserProfile,Stores,Product_category,Product_thumbnail,Products,
                     Product_variants,Product_varient_value,Products,Category,Wish_list,Attributes)
# Register your models here.
class Client_display(admin.ModelAdmin):
    list_display = ("id","name","domain","address")

class UserProfile_display(admin.ModelAdmin):
    list_display = ("id","full_name","email","phone","address","status")

class Categories_display(admin.ModelAdmin):
    list_display = ("id","name","slug","status")

class Store_display(admin.ModelAdmin):
    list_display = ("id","address","post_code","business_email","business_name","business_address")

class Product_diaplay(admin.ModelAdmin):
    list_display = ("id","name","description","slug","status")

class Attributes_display(admin.ModelAdmin):
    list_display = ("id","name","status","product_id")

class WishList_display(admin.ModelAdmin):
    list_display = ("id","user_id","product_id","init_price","created_date")

class Product_category_display(admin.ModelAdmin):
    list_display = ("id","category_id")

class Product_thumbnail_display(admin.ModelAdmin):
    list_display = ("id","name","thumbnail_url","product_variant_id")

class Product_varient_display(admin.ModelAdmin):
    list_display = ("id","price","stock","status","product_id")

class Product_varient_value_display(admin.ModelAdmin):
    list_display = ("id","product_varient_id","value_id")

admin.site.register(UserProfile,UserProfile_display)
admin.site.register(Client,Client_display)
admin.site.register(Stores,Store_display)
admin.site.register(Category,Categories_display)
admin.site.register(Products,Product_diaplay)
admin.site.register(Wish_list,WishList_display)
admin.site.register(Attributes,Attributes_display)
admin.site.register(Product_category,Product_category_display)
admin.site.register(Product_thumbnail,Product_thumbnail_display)
admin.site.register(Product_variants,Product_varient_display)
# admin.site.register(Product_varient_value,Product_varient_value_display)