from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, read_only=False)

    def validate(self, data):
        obj = data.get('phone_number', None)
        context = {
            'status': False,
            'message': 'Phone number is not valid'
        }
        if obj[0] == '+':
            if str(obj)[1:].isdigit:
                if obj.startswith('+998') and len(str(obj)) == 13:
                    pass
                elif obj.startswith('+') and len(str(obj)) == 10:
                    pass
                else:
                    raise ValidationError(context)
            else:
                raise ValidationError(context)
        else:
            raise ValidationError(context)

        return data


class VerifySerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('login', 'login'),
        ('signup', 'signup')
    ], required=True, read_only=False)
    code = serializers.CharField(required=True, read_only=False)
    user_id = serializers.UUIDField(required=True, read_only=False)
    first_name = serializers.CharField(max_length=25, required=False, write_only=False)

    def validate_user_id(self, data):
        if not User.objects.filter(id=data).exists():
            context = {
                'status': False,
                'message': 'User doest found'
            }
            raise ValidationError(context)

        return data

    def validate_first_name(self, name):
        if not str(name).isalpha():
            context = {
                'status': False,
                'message': 'Name is not valid'
            }
            raise ValidationError(context)

        return name

    def validate_code(self, code):
        if len(str(code)) != 6 or not str(code).isdigit():
            context = {
                'status': False,
                'message': 'kod xato kiritildi'
            }
            raise ValidationError(context)

        return code

    def validate(self, data):
        status = data.get('status', None)
        first_name = data.get('first_name', None)
        if status == 'login':
            if first_name:
                context = {
                    'status': False,
                    'message': 'Login qismida firstname kiritilmaydi'
                }
                raise ValidationError(context)
        else:
            if first_name is None:
                context = {
                    'status': False,
                    'message': 'Signup qismida firstname kiritilishi shart'
                }
                raise ValidationError(context)

        return data


class SendCodeAgainSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('login', 'login'),
        ('signup', 'signup')
    ], required=True, read_only=False)
    user_id = serializers.UUIDField(required=True, read_only=False)

    def validate(self, data):
        user_id = data.get('user_id', None)
        if not User.objects.filter(id=user_id).exists():
            context = {
                'status': False,
                'message': 'User doest found'
            }
            raise ValidationError(context)

        return data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'first_name', 'date_of_birth')

        extra_kwargs = {
            "username": {"required": False, "read_only": True},
            "phone_number": {"required": False, "read_only": True}
        }

    def validate(self, data):
        first_name = data.get('first_name', None)
        if first_name and not str(first_name).isalpha():
            context = {
                'status': False,
                'message': 'ismni xato kiritdiz'
            }

            raise ValidationError(context)

        return data
