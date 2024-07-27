from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kombo.models import Kombo
from order.models import CartItem, Order, CREATED
from order.serializers import CartItemListSerializer
from product.models import Product, Ingredient
from user.models import User


class CartItemListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        order = Order.objects.get(user=user, status=CREATED)
        query = order.items.all()
        return query


class CartItemCreateView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get_order(user):
        if Order.objects.filter(user=user, status=CREATED).exists():
            return Order.objects.get(user=user, status=CREATED)
        else:
            order = Order.objects.create(user=user, status=CREATED)
            return order

    def create(self, request, *args, **kwargs):
        user = request.user
        order = self.get_order(user)
        data = request.data
        status = data.get('status', None)
        product_id = data.get('product', None)
        kombo = data.get('kombo', None)
        ingredient_product = data.get('ingredient_product', None)
        ingredient_kombo = data.get('ingredient_kombo', None)
        quantity = data.get('quantity', None)
        user = request.user
        if status == "PRODUCT":
            product = Product.objects.get(id=product_id)
            item = CartItem.objects.create(user=user, status=status, product=product, quantity=quantity)
            order.items.add(item)
        elif status == "GAZAK":
            product = Product.objects.get(id=product_id)
            if not ingredient_product:
                item = CartItem.objects.create(user=user, status=status, product=product, quantity=quantity)
                order.items.add(item)
            else:
                item = CartItem.objects.create(user=user, status=status, product=product, quantity=quantity)
                for just in ingredient_product:
                    ingredient = Ingredient.objects.get(id=just)
                    item.ingredient_product.add(ingredient)
                order.items.add(item)
        elif status == "PIZZA":
            product = Product.objects.get(id=product_id)
            if not ingredient_product:
                item = CartItem.objects.create(user=user, status=status, product=product, quantity=quantity)
                order.items.add(item)
            else:
                item = CartItem.objects.create(user=user, status=status, product=product, quantity=quantity)
                for just in ingredient_product:
                    ingredient = Ingredient.objects.get(id=just)
                    item.ingredient_product.add(ingredient)
                order.items.add(item)
        else:
            kombo = Kombo.objects.get(id=kombo)
            item = CartItem.objects.create(user=user, status=status, kombo=kombo, quantity=quantity)
            order.items.add(item)
            for just in ingredient_kombo:
                pro = Product.objects.get(id=just)
                item.ingredient_kombo.add(pro)


        return Response(self.get_serializer(item).data)

