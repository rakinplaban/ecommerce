from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes 
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer 
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from rest_framework import generics
# Create your views here.

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
def allproducts(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
   
@api_view(['GET','POST'])
@renderer_classes([BrowsableAPIRenderer,JSONRenderer])
def allclients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)