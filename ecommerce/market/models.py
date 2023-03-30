from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=70)
    domain = models.CharField(max_length=70)
    address = models.CharField(max_length=70)

class UserProfile(models.Model):
    full_name = models.CharField(max_length=70)
    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=62)
    status = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_store_admin = models.BooleanField(default=False)
    remember_token = models.CharField(max_length=100,null=True,blank=True)
    profile_image_url = models.URLField(null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
  


class Stores(models.Model):
    address = models.CharField(max_length=70)
    post_code = models.CharField(max_length=10)
    business_email = models.EmailField()
    business_name = models.CharField(max_length=70)
    business_address = models.CharField(max_length=70)
    is_active = models.BooleanField(default=True)
    is_varified = models.BooleanField(default=False)
    user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)

class Products(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    slug = models.SlugField()
    store_id = models.ForeignKey(Stores,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    bookmarked = models.ManyToManyField(UserProfile,through='Wish_list',related_name="bookmarked",blank=True,default=None)

class Wish_list(models.Model):
    created_date = models.DateField(auto_now_add=True)
    init_price =  models.FloatField()
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField()
    store_id = models.ForeignKey(Stores,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    product = models.ManyToManyField(Products,through='Product_category',related_name="product",blank=True,default=None)


class Product_category(models.Model):
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)


class Product_variants(models.Model):
    price = models.FloatField()
    stock = models.IntegerField()
    status = models.BooleanField(default=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)



class Product_thumbnail(models.Model):
    name = models.CharField(max_length=70)
    thumbnail_url = models.URLField()
    product_variant_id = models.ForeignKey(Product_variants,on_delete=models.CASCADE)


class Attributes(models.Model):
    name = models.CharField(max_length=70)
    status = models.BooleanField(default=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)


class Value(models.Model):
    value = models.CharField(max_length=70)
    attribute_id = models.ForeignKey(Attributes,on_delete=models.CASCADE)

class Product_varient_value:
    product_variant_id = models.ForeignKey(Product_variants,on_delete=models.CASCADE)
    value_id = models.ForeignKey(Value,on_delete=models.CASCADE)