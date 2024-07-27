from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from common.models import BaseModel, Address
from kombo.models import Kombo
from product.models import Product, Ingredient
from user.models import User


CREATED, IN_PROGRESS, DELIVERED, CANCELLED, FINISHED = ('CREATED', 'IN_PROGRESS', 'DELIVERED', 'CANCELLED', 'FINISHED')
KICHKINA, ORTACHA, KATTA = ('KICHKINA', "O'RTACHA", "KATTA")

class CartItem(BaseModel):
    CARTSTATUS = (
        ('PRODUCT', 'PRODUCT'),
        ('KOMBO', 'KOMBO'),
        ('PIZZA', 'PIZZA'),
        ('GAZAK', 'GAZAK')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitems')

    status = models.CharField(max_length=20, choices=CARTSTATUS)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, help_text="Kombo bo'lsa bo'sh qoldiring")
    kombo = models.ForeignKey(Kombo, on_delete=models.CASCADE, null=True, blank=True, help_text="faqat kombo uchun kiriting")

    ingredient_product = models.ManyToManyField(Ingredient, blank=True, help_text="faqat pizza va gazak uchun kiriting")
    ingredient_kombo = models.ManyToManyField(Product, blank=True, help_text="faqat kombo uchun kiriting",
                                              related_name="just")

    quantity = models.PositiveIntegerField()
    subtotal = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.phone_number} {self.product.name}"

    class Meta:
        db_table = 'cartitem'
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'


    def save(self, *args, **kwargs):
        if self.status == "PRODUCT" or self.status == "GAZAK":
            self.subtotal = self.product.price * self.quantity
        elif self.status == "PIZZA":
            total_price = self.product.price
            if self.ingredient_product:
                pizza_shape = ItemThrough.objects.get(cartitem__id=self.id).pizza_shape
                if pizza_shape == KICHKINA:
                    for item in self.ingredient_product.all():
                        total_price += item.small_price
                if pizza_shape == ORTACHA:
                    for item in self.ingredient_product.all():
                        total_price += item.medium_price
                if pizza_shape == KATTA:
                    for item in self.ingredient_product.all():
                        total_price += item.big_price
                self.subtotal = total_price * self.quantity
        super().save(*args, **kwargs)


class ItemThrough(BaseModel):
    PIZZA_SHAPE = (
        ('KICHKINA', 'KICHKINA'),
        ("O'RTACHA", "O'RTACHA"),
        ('KATTA', 'KATTA')
    )
    PIZZA_VOLUME = (
        ('YUPQA', 'YUPQA'),
        ('QALIN', 'QALIN')
    )

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    cartitem = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="itemthrough")

    is_pizza = models.BooleanField(default=False)
    pizza_shape= models.CharField(max_length=20, choices=PIZZA_SHAPE, null=True, blank=True,
                                  verbose_name="Pitsa o'lchami", help_text="Bu fieldga faqat pitsa statusi uchun kiritasiz")
    pizza_volume = models.CharField(max_length=20, choices=PIZZA_VOLUME, null=True, blank=True,
                                    verbose_name="Pitsa ko'rinishi", help_text="Bu fieldga faqat pitsa statusi uchun kiritasiz")

    def __str__(self):
        return str(self.cartitem)

    class Meta:
        db_table = 'itemthrough'
        verbose_name = 'ItemThrough'
        verbose_name_plural = 'ItemThrough'


class Order(BaseModel):
    ORDERSTATUS = (
        ('CREATED', 'CREATED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('DELIVERED', 'DELIVERED'),
        ('CANCELLED', 'CANCELLED'),
        ('FINISHED', 'FINISHED')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(max_length=20, choices=ORDERSTATUS, default='CREATED')
    items = models.ManyToManyField('CartItem', through=ItemThrough, blank=True)
    # items_kombo = models.ManyToManyField('CartItem_kombo', through=KomboThrough, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.PositiveSmallIntegerField(null=True, blank=True)
    time_of_order = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if not self.user:
            raise ValidationError("Userni kiriting")
        user = self.user
        if not self.id:
            if self.status == CREATED:
                if Order.objects.filter(user=user, status=CREATED).exists():
                    raise ValidationError("Sizda order mavjud...")
        else:
            if self.status == CREATED:
                if Order.objects.filter(Q(user=user) & Q(status=CREATED) & ~Q(id=self.id)).exists():
                    raise ValidationError("Sizda order mavjud...")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        total_price = 0
        for item in self.items.all():
            total_price += item.subtotal
        self.total_price = total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} buyurtman raqami: {self.order_number} holati: {self.status}"

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

