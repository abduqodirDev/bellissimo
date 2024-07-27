from rest_framework import serializers

from product.models import Product, ProductChild, Ingredient


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')
        ref_name = "productserializerproductapp"

    def to_representation(self, instance):
        if not instance.price:
            price = instance.product_child.price_small_pizza
            instance.price = price
        return super().to_representation(instance)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'image', 'status', 'price_status', 'small_price', 'medium_price', 'big_price', 'in_stock')


class ProductChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductChild
        fields = ('status', 'pizza_type', 'price_small_pizza', 'price_medium_pizza',
                  'price_big_pizza', 'ingredient_count', 'ingredient')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        query = instance.ingredient.ingredient.all()
        serializer = IngredientSerializer(query, many=True)
        data['ingredient'] = serializer.data
        return data


class ProductDetailSerializer(serializers.ModelSerializer):
    category  = serializers.SerializerMethodField('get_category')
    product_child = ProductChildSerializer()

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image', 'in_stock', 'product_child')

    def get_category(self, obj):
        return obj.category.name if obj.category else None
