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
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
  


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
    ordered = models.ManyToManyField(UserProfile,through='Orders',related_name="ordered",blank=True,default=None)

class Wish_list(models.Model):
    created_date = models.DateField(auto_now_add=True)
    init_price =  models.FloatField()
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)

class Orders(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active_status = models.BooleanField(default=True)
    user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)


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
    cart_added = models.ManyToManyField(UserProfile,through='Cart',related_name="cart_added",blank=True,default=None)



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

class Cart(models.Model):
    user_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product_variant_id = models.ForeignKey(Product_variants,on_delete=models.CASCADE)
    amount = models.IntegerField()
    initial_price = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


class Payment_Method(models.Model):
    option = models.CharField(max_length=45)
    billing_address = models.CharField(max_length=45)
    security_code = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    minimum_amount = models.DecimalField(max_digits=10,decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=10,decimal_places=2)
    method_status = models.BooleanField(default=True)
    currency = models.CharField(max_length=45)
    payment = models.ManyToManyField(Orders,through='Payment_Stauts',related_name="payment")


class Payment_Stauts(models.Model):
    progress = models.CharField(max_length=45)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    payment_id = models.ForeignKey(Payment_Method,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE)
   
    
class Shiping_Method(models.Model):
    service_type = models.CharField(max_length=45)
    deadline = models.CharField(max_length=45)
    transportation_cost = models.FloatField(null=True,blank=True)
    location = models.CharField(max_length=45)
    availability_status = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    shiping = models.ManyToManyField(Orders,through='Shiping_Status',related_name="shiping")


class Shiping_Status(models.Model):
    progress = models.CharField(max_length=45,null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    shiping_id = models.ForeignKey(Shiping_Method,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE)
