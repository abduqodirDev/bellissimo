import uuid
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from config.settings import CODE_CONFIRMATION_TIME
from user.validators import check_phone_validator, check_code_validator


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=20, unique=True, validators=[check_phone_validator, ])
    date_of_birth = models.DateField(null=True, blank=True)

    def clean_username(self):
        if not self.username:
            while True:
                username = "bellissimo-" + str(uuid.uuid4()).split('-')[-1]
                if User.objects.filter(username=username).exists():
                    continue
                else:
                    break
            self.username = username

    def clean_password(self):
        if not self.password:
            while True:
                password = "bellissimo-" + str(uuid.uuid4()).split('-')[-1]
                if User.objects.filter(password=password).exists():
                    continue
                else:
                    break
            self.password = password

    def clean(self):
        self.clean_username()
        self.clean_password()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number.__str__()


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=6, validators=[check_code_validator, ])
    status = models.BooleanField(default=False)
    time = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userconfirmation')

    def save(self, *args, **kwargs):
        if not self.time:
            self.time = datetime.now() + timedelta(minutes=CODE_CONFIRMATION_TIME)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

