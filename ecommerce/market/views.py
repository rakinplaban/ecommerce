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



@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_payment_method(request):
    if request.method == 'POST':
        try:
            payment_method = Payment_Method.objects.create(
                user_acc=request.user.userprofile,
                billing_address=request.data['billing_address'],
                security_code=request.data['security_code'],
                country=request.data['country'],
                minimum_amount=request.data['minimum_amount'],
                maximum_amount=request.data['maximum_amount'],
                method_status=request.data['method_status'],
                currency=request.data['currency'],
            )
            serializer = PaymentMethodSerializer(payment_method, many=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def selected_payment(request):
    try:
        payment_method = Payment_Method.objects.get(user_acc=request.user.userprofile)
        serializer = PaymentMethodSerializer(payment_method)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    


@api_view(['PUT'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_payment_method(request,id):
    if request.method == 'PUT':
        try:
            payment_method = Payment_Method.objects.get(id=id)
            payment_method.billing_address=request.data['billing_address'],
            payment_method.security_code=request.data['security_code'],
            payment_method.country=request.data['country'],
            payment_method.minimum_amount=request.data['minimum_amount'],
            payment_method.maximum_amount=request.data['maximum_amount'],
            payment_method.method_status=request.data['method_status'],
            payment_method.currency=request.data['currency'],
            payment_method.save()
            serializer = PaymentMethodSerializer(payment_method)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def payment_status_activate(request,id,order_pk):
    if request.method == 'POST':
        try:
            payment = Payment_Method.objects.get(id=id)
            order = Orders.objects.get(id=order_pk)
            payment_initiate = Payment_Stauts.objects.create(
                progress = request.POST['progress'],
                charges = request.POST['charges'],
                created_date = request.POST['created_date'],
                updated_date = request.POST['updated_date'],
                payment_id = payment,
                order_id = order
            )

            serializers = PaymentStatusSerializer(payment_initiate, many=True)
            return Response(serializers.data,status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def view_payment_status(request,id):
    try:
        payment_status = Payment_Stauts.objects.get(id=id)
        serializer = PaymentStatusSerializer(payment_status, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_payment_status(request,id):
    if request.method == 'PUT':
        try:
            payment_status = Payment_Stauts.objects.get(id=id)
            payment_status.progress = request.data['progress'],
            payment_status.charges = request.data['charges'],
            payment_status.created_date = request.data['created_date'],
            payment_status.updated_date = request.data['updated_date'],
            payment_status.save()
            serializer = PaymentStatusSerializer(payment_status)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
