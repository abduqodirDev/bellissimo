from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from product.models import Product, Category
from product.serializer import ProductSerializer, ProductDetailSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        context = {}
        for cate in Category.objects.all():
            if cate.name == 'kombo':
                continue
            name = cate.name
            products = Product.objects.filter(category=cate)
            serializer = self.get_serializer(products, many=True)
            context[name] = serializer.data

        return Response(context)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug', None)
        if Product.objects.filter(slug=slug).exists():
            return Product.objects.get(slug=slug)
        else:
            context = {
                'status': False,
                'message': 'Product does not found'
            }
            raise ValidationError(context)

    def retrieve(self, request, *args, **kwargs):
        objects = self.get_object()
        serializer = self.get_serializer(objects)
        context = {
            'status': True,
            'data': serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)



