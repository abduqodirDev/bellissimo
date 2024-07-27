from rest_framework import serializers

from common.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'address', 'name_address')


class AddAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"

        extra_kwargs = {
            'user': {'required': False}
        }
