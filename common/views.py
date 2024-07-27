from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Address
from common.serializers import AddressSerializer, AddAddressSerializer


class ListDeleteAddressView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        query = Address.objects.filter(user=user)
        serializer = AddressSerializer(query, many=True)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        address_id = data.get('id', None)
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            context = {
                'status': False,
                'message': 'Bu idga tegishli manzil topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if address.user != user:
            context = {
                'status': False,
                'message': 'Bu manzil sizga tegishli emas'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        address.delete()
        context = {
            'status': True,
            'message': 'Address o\'chirilib tashlandi'
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)


class AddAddressView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddAddressSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

