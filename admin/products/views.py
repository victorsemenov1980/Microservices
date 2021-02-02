from django.shortcuts import render
from django.http import JsonResponse

import random
from rest_framework import viewsets,status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .producer import publish
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout


#entire viewset got to be protected with Login

class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):#/api/products
        '''
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response (serializer.data)
        '''
       
        publish('product list requested',1)
        
        '''
        Here we got to extract response from Redis and send
        it to frontend
        '''
        return JsonResponse({
                        'message':'Here got to be response from Redis'
     
                            })
    
    def create(self, request):#/api/products
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product created',serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
 
    def retrieve (self, request, pk=None):#/api/products/<str:id>
        product=Product.objects.get(id=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    
   
    def update (self, request, pk=None):#/api/products/<str:id>
        product=Product.objects.get(id=pk)
        serializer=ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product updated',serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
   
    def destroy (self, request, pk=None):#/api/products/<str:id>
        product=Product.objects.get(id=pk)
        product.delete()
        publish('product deleted',pk)
        return Response(status=status.HTTP_204_NO_CONTENT)






