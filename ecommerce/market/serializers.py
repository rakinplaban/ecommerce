from rest_framework import serializers
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from . import models
from .models import (Client,User,UserProfile,Stores,Product_category,Product_thumbnail,Value, Cart, Orders,
                     Product_variants,Product_varient_value,Products,Category,Wish_list,Attributes,
                     Payment_Stauts,Payment_Method,Shiping_Method,Shiping_Status)
# Create your serializers here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        

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
        fields = ['created_date','init_price','product','user']
  

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


class CartSerializer(serializers.ModelSerializer):
    product = serializers.RelatedField(source='product_variant_id',read_only=True)
    user = serializers.RelatedField(source='user_id',read_only=True)
    class Meta:
        model = Cart
        fields = ['product','user','amount','initial_price','created_date','updated_date']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField(source='user_id',read_only=True)
    product = serializers.RelatedField(source='product_id',read_only=True)
    class Meta:
        model = Orders
        fields = ['user','product','active_status','created_date','updated_date']


class PaymentMethodSerializer(serializers.ModelSerializer):
    user_acc = serializers.RelatedField(source='user_acc',read_only=True)
    class Meta:
        model = Payment_Method
        fields = ['option','billing_address','security_code','country','minimum_amount', 'maximum_amount','method_status','currency']


class PaymentStatusSerializer(serializers.ModelSerializer):
    payment = serializers.RelatedField(source='payment_id',read_only=True)
    order = serializers.RelatedField(source='order_id',read_only=True)
    class Meta:
        model = Payment_Stauts
        fields = ['progress','created_date','updated_date']


class ShipingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shiping_Method
        fields = ['service_type','deadline','transportation_cost','location','availability_status','created_date','updated_date']


class ShipingStatusSerializer(serializers.ModelSerializer):
    shiping = serializers.RelatedField(source='shiping_id',read_only=True)
    order = serializers.RelatedField(source='order_id',read_only=True)
    class Meta:
        model = Shiping_Status
        fields = ['progress','created_date','updated_date']
