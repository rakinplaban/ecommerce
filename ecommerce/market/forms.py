from django import forms

from .models import *

class Client_form(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','domain','address' ]

        labels = {
            'name' : 'Name*',
            'domain' : 'Domain',
            'address' : 'Address*'
        }

        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Name of Client',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'domain' : forms.TextInput(attrs={
                'class' : 'form-control',
                'rows' : 1,
                'cols' : 100,
                'type' : 'address',
                # 'id' : 'upload_custom',
            }),
        }


class Profile_form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name','phone','address','email', 'profile_image_url','client_id']

        labels = {
            'full_name' : 'Full Name*',
            'phone' : 'Phone*',
            'email' : 'Email*',
            'address' : 'Address*',
            'profile_image_url' : '',
        }

        widgets = {
            'full_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title of image',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'phone' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title of image',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'email' : forms.EmailInput(),

            'profile_image_url' : forms.ClearableFileInput(attrs={
                'class' : 'dropify',
                'rows' : 1,
                'cols' : 100,
                'type' : 'file',
                'multiple' : True,
                'data-height' : 100,
                # 'id' : 'upload_custom',
            }),

            'address' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'address',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text',
            }),

            
        }

class StoresForm(forms.ModelForm):
    class Meta:
        model = Stores
        fields = ['address', 'post_code', 'business_email', 'business_name', 'business_address', 'is_active', 'is_varified', 'user_id', 'client_id']

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'slug', 'store_id', 'status']


class ProductThumbnailForm(forms.ModelForm):
    class Meta:
        model = Product_thumbnail
        fields = ['name', 'thumbnail_url', 'product_variant_id']  

class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        fields = ['value', 'attribute_id']


class AttributesForm(forms.ModelForm):
    class Meta:
        model = Attributes
        fields = ['name', 'status', 'product_id']     

class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'status', 'parent_id']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['parent'] = Category.objects.all()

        labels = {
            'name' : 'Name',
            'slug' : 'URL',
            'status' : 'Status',	
            'parent_id' : 'Parent'
        }

        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title of Category',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'slug' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Short URL of image',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            # 'parent' : forms.Select(attrs={
            #     'class' : 'dropdown-toggle',
            #     'type' : 'select'
            # }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({"class": "form-control"})
        # or iterate over field to add class for each field
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"form-control"})