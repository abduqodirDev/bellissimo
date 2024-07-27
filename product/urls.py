from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('product-list/', ProductListView.as_view()),
    path('<slug:slug>/', ProductDetailView.as_view()),
]
