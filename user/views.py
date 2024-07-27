import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from user.models import User, UserConfirmation
from user.serializers import LoginSerializer, VerifySerializer, SendCodeAgainSerializer, ProfileSerializer
from user.validators import create_code


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data.get('phone_number', None)

        if User.objects.filter(phone_number=phone_number).exists():
            code = create_code()
            user = User.objects.get(phone_number=phone_number)
            UserConfirmation.objects.create(code=code, user=user)
            context = {
                'status': 'Login',
                'messages': 'Code successfully sended',
                'user_id': user.id
            }

            return Response(context)

        phone_number = serializer.validated_data.get('phone_number', None)
        user = User.objects.create(phone_number=phone_number, is_active=False)
        code = create_code()
        UserConfirmation.objects.create(code=code, user=user)
        context = {
            'status': 'Signup',
            'messages': 'Code successfully sended',
            'user_id': user.id
        }

        return Response(context)


class VerifyView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = VerifySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id', None)
        status = serializer.validated_data.get('status', None)
        code = serializer.validated_data.get('code', None)
        first_name = serializer.validated_data.get('first_name', None)
        user = User.objects.get(id=user_id)
        verify_codes = user.userconfirmation.all()

        if not verify_codes.filter(status=False , time__gte=datetime.datetime.now()).exists():
            context = {
                'status': False,
                'message': 'Vaqtingiz tugadi'
            }

            return Response(context, status=400)

        verify = verify_codes.filter(status=False , time__gte=datetime.datetime.now())[0]

        if verify.code != code:
            context = {
                'status': False,
                'message': 'Code xato'
            }

            return Response(context, status=400)

        verify.status=True
        verify.save()

        if status == 'login':
            refresh = RefreshToken.for_user(user)
            context = {
                'status': True,
                'case': 'login',
                'message': "code tasdiqlandi",
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        else:
            user.first_name = first_name
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            context = {
                'status': True,
                'case': 'signup',
                'message': "code tasdiqlandi",
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }

        return Response(context)


class SendCodeAgainView(APIView):

    @staticmethod
    def check_confirmation_code(user):
        if user.userconfirmation.filter(status=False, time__gte=datetime.datetime.now()).exists():
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SendCodeAgainSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data.get('status', None)
        user_id = serializer.validated_data.get('user_id', None)
        user = User.objects.get(id=user_id)
        code = create_code()

        if status == 'login':
            if self.check_confirmation_code(user):
                context = {
                    'status': False,
                    'message': 'Siz qayta kod jo\'nata ololmaysiz'
                }

                return Response(context, status=400)

            UserConfirmation.objects.create(code=code, user=user)
            context = {
                'status': 'login',
                'message': 'Code successfully sended',
                'user_id': user.id
            }

            return Response(context)

        if user.is_active == True or user.first_name:
            context = {
                'status': False,
                'message': 'Siz avval ro\'yxatdan o\'tgansiz'
            }

            return Response(context, status=400)

        if self.check_confirmation_code(user):
            context = {
                'status': False,
                'message': 'Siz qayta kod jo\'nata ololmaysiz'
            }

            return Response(context, status=400)

        UserConfirmation.objects.create(code=code, user=user)
        context = {
            'status': 'signup',
            'message': 'Code successfully sended',
            'user_id': user.id
        }

        return Response(context)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        first_name = data.get('first_name', None)
        date = data.get('date_of_birth', None)

        serializer = ProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if len(data) > 2 or (len(data)==2 and (not first_name or not date)) or (len(data)==1 and (not first_name and not date)):
            context = {
                'status': False,
                'message': "Malumotlar xato kiritildi"
            }
            return Response(context, status=400)

        if first_name:
            user.first_name = first_name
        if date:
            user.date_of_birth = date

        serializer = ProfileSerializer(user)

        user.save()
        context = {
            'status': True,
            'message': 'User successfully updated',
            'data': serializer.data
        }
        return Response(context)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        refresh_token = data.get('refresh', None)
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except Exception as e:
            raise ValidationError(e)

        context = {
            'status': True,
            'message': 'logged out'
        }

        return Response(context)


# class LogoutView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_class(self):
#         return None
#
#     def delete(self, request, *args, **kwargs):
#         request.user.auth_token.delete()
#         return Response(status=204)

