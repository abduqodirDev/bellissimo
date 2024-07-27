from django.urls import path

from order.views import CartItemListView, CartItemCreateView

urlpatterns = [
    path('cartitem-list/', CartItemListView.as_view()),
    path('cartitem-create/', CartItemCreateView.as_view()),
]
