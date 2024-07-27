from django.urls import path

from common.views import ListDeleteAddressView, AddAddressView

urlpatterns = [
    path('address-list-delete/', ListDeleteAddressView.as_view()),
    path('address-create/', AddAddressView.as_view()),
]
