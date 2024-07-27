from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kombo.models import Kombo
from kombo.serializer import KomboSerializer, KomboDetailSerializer


class KomboListView(ListAPIView):
    queryset = Kombo.objects.all()
    serializer_class = KomboSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        query = Kombo.objects.filter(in_stock=True)
        return query

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        kombo_count = len(self.get_queryset())
        context = {
            "status": status.HTTP_200_OK,
            "kombo_count": kombo_count,
            "data": serializer.data
        }
        return Response(context)


class KomboDetailView(RetrieveAPIView):
    queryset = Kombo.objects.all()
    serializer_class = KomboDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'pk'
