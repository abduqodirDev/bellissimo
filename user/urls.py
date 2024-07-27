from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView, TokenVerifyView

from user.views import LoginView, VerifyView, SendCodeAgainView, ProfileView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('refresh-token/', TokenRefreshView.as_view()),
    path("check-token/", TokenVerifyView.as_view()),

    path('verify/', VerifyView.as_view()),
    path('send-code-again/', SendCodeAgainView.as_view()),
    path('profile/', ProfileView.as_view()),
]
