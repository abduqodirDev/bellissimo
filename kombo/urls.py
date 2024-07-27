from django.urls import path

from kombo.views import KomboListView, KomboDetailView

urlpatterns = [
    path('kombo-list/', KomboListView.as_view()),
    path('<uuid:pk>/', KomboDetailView.as_view()),
]
