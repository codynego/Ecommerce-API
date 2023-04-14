from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class CategoryList(APIView):
    def get(self, request):
        category = Category.objects.all()
        categoryName = request.query_params.get('category')
        search = request.query_params.get('search')
        if categoryName:
            category = category.filter(name=categoryName)
        if search:
            category = category.filter(name__contains=search)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    def get(self, request):
        product = Product.objects.all()
        try:
            productName = request.query_params.get('name')
            categoryName = request.query_params.get('category')
            price = request.query_params.get('price')
            search = request.query_params.get('search')
        except KeyError:
            error_message = {'error': 'parameter not found'}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        if productName:
            product = product.filter(name=productName)
        if categoryName:
            product = product.filter(category__name=categoryName)
        if price:
            product = product.filter(price__lte=price)
        if search:
            product = product.filter(name__startswith=search)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            category_name = request.data.get('category')
            if not category_name:
                return Response({'category_name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = Category.objects.get(name=category_name['name'])
            except Category.DoesNotExist:
                category = Category.objects.create(name=category_name['name'])
                category.save()
                serializer.validated_data['category'] = category
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

