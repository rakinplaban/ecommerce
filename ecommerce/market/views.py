from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (api_view, renderer_classes , 
                                       authentication_classes , permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer 
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .forms import *
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from datetime import datetime
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status':200, 'token':token.key})
    return Response({'status':401, 'message':'Invalid credentials'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the token
    token.delete()
    
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username= serializer.data['username'])
            token , _ = Token.objects.get_or_create(user=user)
            return Response({'status':200,'payload': serializer.data, 'token':str(token)})
        return Response(serializer.errors, status=401)

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def  allusers(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def all_products(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

   
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def view_category(request):
    if request.method == 'GET':
        clients = Category.objects.all()
        serializer = CategoriesSerializer(clients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def product_pricing(request,id):
    try:
        if request.method == 'GET':
            clients = Product_variants.objects.get(product_id=id)
            serializer = ProductVariantSerializer(clients, many=True)
            return Response(serializer.data)
    except:
        return Response({'status':404,'message':'Product not found'})
    

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def product_thumbnail(request,id):
    if request.method == 'GET':
        try:
            product_thumbnails = Product_thumbnail.objects.get(product_variant_id=id)
            serializer = ProductThumbnailSerializer(product_thumbnails, many=True)
            return Response(serializer.data)
        except:
            return Response({'status':404,'message':'Product not found'})
        
    
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def store_info(request,id):
    if request.method == 'GET':
        try:
            product_thumbnails = Stores.objects.get(id=id)
            serializer = StoreSerializer(product_thumbnails, many=True)
            return Response(serializer.data)
        except:
            return Response({'status':404,'message':'No store found!'})
        

@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_wishlist(request,id):
    if request.method == 'POST':
        try:
            product_item = Products.objects.get(id=id)
            wishlist_item = Wish_list.objects.create(
                product_id=product_item,
                user_id=request.user.userprofile,
                created_date = datetime.now(),
            )
            serializer = WishListSerializer(wishlist_item, many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except:
            return Response({'status':404,'message':'No product found!'})
        
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_wishlist(request):
    if request.method == 'GET':
        try:
            wishlist_items = Wish_list.objects.filter(user_id=request.user.id)
            serializer = WishListSerializer(wishlist_items, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'status':404,'message':'No user found!'})
        
    
@api_view(['DELETE'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request,id):
    if request.method == 'DELETE':
        try:
            wishlist_item = Wish_list.objects.get(id=id)
            wishlist_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'status':404,'message':'No user found!'})
        
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@authentication_classes([TokenAuthentication])
def add_to_cart(request,id):
    if request.method == 'POST':
        try:
            product_variant = Product_variants.objects.get(id=id)
            initial_price = product_variant.price
            cart_item = Cart.objects.create(
                 user_id=request.user.userprofile,
                product_variant_id=product_variant,
                amount=request.data['amount'],
                initial_price=initial_price
            )
            serializer = CartSerializer(cart_item, many=True)
            return Response(serializer.data,serializer.data, status=status.HTTP_201_CREATED)
        except Product_variants.DoesNotExist:
            return Response({'status': 404, 'message': 'No product found!'})
        

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def view_cart(request):
    try:
        if request.method == 'GET':
            cart_items = Cart.objects.filter(user_id=request.user.id)
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'status':404,'message':'No user found!'})
    

@api_view(['PUT'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])

def update_cart(request,id):
    try:
        # if request.method == 'POST':
        cart_item = Cart.objects.get(id=id)
        cart_item.amount = request.data['amount']
        cart_item.save()
        serializer = CartSerializer(cart_item, data=request.data, partial=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    except:
        return Response({'status':404,'message':'No item found!'})
    

@api_view(['DELETE'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_cart_item(request, id):
    if request.method == 'DELETE':
        try:
            cart_item = Cart.objects.get(id=id)
            cart_item.delete()
            return Response({'status': 200, 'message': 'Cart item deleted successfully.'})
        except Cart.DoesNotExist:
            return Response({'status': 404, 'message': 'No cart item found with the provided ID.'})
    

@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_order(request,id):
    if request.method == 'POST':
        try: 
            product = Products.objects.get(id=id)
            order_item = Orders.objects.create(
                user_id=request.user.userprofile,
                product_id=product,
            )
            serializer = OrderSerializer(order_item, many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except:
            return Response({'status':404,'message':'Product not found!'})  
    

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def track_orders(request):
    if request.method == 'GET':
        try:
            order_item = Orders.objects.filter(user_id=request.user.id)
            serializer = OrderSerializer(order_item, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'status':404,'message':'No user found!'})
    

@api_view(['DELETE'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cancel_order(request,id):
    if request.method == 'DELETE':
        try:
            order_item = Orders.objects.get(id=id)
            order_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_410_GONE)
