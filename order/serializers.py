from rest_framework import serializers

from kombo.models import Kombo
from order.models import CartItem
from product.models import Product, Ingredient


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']
        ref_name = "productserializerorderapp"

class KomboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kombo
        fields = ['id', 'name']
        ref_name = "komboserializerorderapp"

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class KomboProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']

class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    kombo = KomboSerializer(required=False)
    ingredient_product = IngredientSerializer(many=True, read_only=True, required=False)
    ingredient_kombo = KomboProductSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',  # Agar user maydoni ham kerak bo'lsa
            'status',
            'product',
            'kombo',
            'ingredient_product',
            'ingredient_kombo',
            'quantity',
            'subtotal'
        ]



