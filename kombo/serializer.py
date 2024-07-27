from rest_framework import serializers

from kombo.models import Kombo, ChildKombo, ChildKomboItem
from product.models import Product


class KomboSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kombo
        fields = ('name', 'description', 'price', 'discount', 'discount_price', 'image')
        ref_name = "komboserializerkomboapp"


class ProductSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'image')


class KomboChildItemSerializer(serializers.ModelSerializer):
    product = ProductSerialzier()

    class Meta:
        model = ChildKomboItem
        fields = ('product', 'is_pizza', 'overprice', 'size')


class KomboChildSerializer(serializers.ModelSerializer):
    product = KomboChildItemSerializer(source='childkomboitem_set', many=True)

    class Meta:
        model = ChildKombo
        fields = ('status', 'quantity', 'product')


class KomboDetailSerializer(serializers.ModelSerializer):
    kombo_child = serializers.SerializerMethodField('KomboChild', required=False)

    class Meta:
        model = Kombo
        fields = ('name', 'description', 'image', 'price', 'discount', 'discount_price', 'kombo_child')

    def KomboChild(self, obj):
        objects = obj.kombochild.all()
        serializer = KomboChildSerializer(objects, many=True).data
        return serializer
