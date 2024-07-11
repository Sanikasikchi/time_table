from rest_framework import serializers, viewsets, routers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect, HttpResponse

# from backend.customer.models import Customer
# from backend.product.models import Products



# class ProductsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = '__all__'


# class Product(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializers


# class CustomerSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'


# class Customer(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializers


# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def get(request):
#     pro = Products.objects.all()
#     context = {
#         "message": "success",
#         "data": []
#     }
#     for data in pro:
#         context["data"].append({
#             "id": data.id,
#             "pro_name": data.pro_name,
#         })
#     return Response(context)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def post(request):
#     price = int(request.POST.get('price'))
#     pro_name = request.POST.get('pro_name')

#     if not price:
#         return Response({
#             "message": "FAILURE",
#             "data": "price not provided"
#         })

#     if not pro_name:
#         return Response({
#             "message": "FAILURE",
#             "data": "pro_name not provided"
#         })
#     return Response({"message": "success"})
