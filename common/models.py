import uuid

from django.db import models
from django.db.models import UniqueConstraint


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(BaseModel):
    from django.contrib.auth import get_user_model
    user = get_user_model()

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="address")

    address = models.CharField(max_length=250)
    bino_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="uy/bino raqami")
    office_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="uy/office raqami")
    podyezt = models.CharField(max_length=10, blank=True, null=True)
    qavat = models.CharField(max_length=10, blank=True, null=True)
    door_number = models.CharField(max_length=10, null=True, blank=True, verbose_name="eshik raqami")
    name_address = models.CharField(max_length=250, blank=True, null=True, verbose_name="manzil nomi")
    note_address = models.CharField(max_length=250, blank=True, null=True, verbose_name="manzilga izoh")

    def __str__(self):
        return f"{self.address} ({self.name_address})"

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        constraints = [
            UniqueConstraint(
                fields=['user', 'address', 'name_address'],
                name='address uniqe'
            )
        ]

