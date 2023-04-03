from rest_framework import serializers
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from . import models
from .models import (Client,User,UserProfile,Stores,Product_category,Product_thumbnail,Value,
                     Product_variants,Product_varient_value,Products,Category,Wish_list,Attributes)
# Create your serializers here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        

class ClientSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Client
        fields = ['name' , 'domain' , 'address' ]

class UserProfileSerializer(serializers.ModelSerializer):
    client = serializers.RelatedField(source='client_id',read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone' ,'address' ,'status' ,'email', 'profile_image_url','remember_token','user']
    

class StoreSerializer(serializers.ModelSerializer):
    user_profile = serializers.RelatedField(source='user_id',read_only=True)
    client = serializers.RelatedField(source='client_id',read_only=True)
    class Meta:
        model = Stores
        fields = ['address', 'post_code', 'business_email','business_name',
                'business_address', 'is_active' , 'is_varified' ]


class CategoriesSerializer(serializers.ModelSerializer):
    store = serializers.RelatedField(source='store_id',read_only=True)
    client = serializers.RelatedField(source='client_id',read_only=True)
    parent = serializers.RelatedField(source='parent_id',read_only=True)
    class Meta:
        model = Category
        fields = ['name','slug','status']


class ProductSerializer(serializers.ModelSerializer):
    bookmarked = UserProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ['name', 'description', 'slug', 'store_id', 'status', 'bookmarked']


class WishListSerializer(serializers.ModelSerializer):
    product = serializers.RelatedField(source='product_id',read_only=True)
    user = serializers.RelatedField(source='user_id',read_only=True)
    class Meta:
        model = Wish_list
        fields = ['created_date','init_price']
  

class AttributesSerializer(serializers.ModelSerializer):
    product = serializers.RelatedField(source='product_id',read_only=True)
    class Meta:
        model = Attributes
        fields = ['name','status']


class ProductCategorySerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset = Products.objects.all())
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())
    class Meta:
        model = Product_category
        fields = ['product_id' ,'category_id']
   


class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.RelatedField(source='product_id',read_only=True)
    class Meta:
        model = Product_variants
        fields = ['price','stock','status']


class ProductThumbnailSerializer(serializers.ModelSerializer):
    product_varient = serializers.RelatedField(source='product_varient_id',read_only=True)
    class Meta:
        model = Product_thumbnail
        fields = ['name','thumbnail_url']


class ValueSerializer(serializers.ModelSerializer):
    attribute = serializers.RelatedField(source='attribute_id',read_only=True)
    class Meta:
        model = Value
        fields = ['value']


class ProductVarientValueSerializer(serializers.ModelSerializer):
    product_varient_id = serializers.PrimaryKeyRelatedField(queryset = Product_variants.objects.all())
    value_id = serializers.PrimaryKeyRelatedField(queryset = Value.objects.all())
    class Meta:
        model = Product_varient_value
        fields = ['product_variant_id','value_id']
