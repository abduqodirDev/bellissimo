from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

from common.models import BaseModel
from product.models import Category, Product


class Kombo(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=250)
    price = models.PositiveIntegerField(validators=[MinValueValidator(999), MaxValueValidator(999999)])
    discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    discount_price = models.PositiveIntegerField(validators=[MinValueValidator(999), MaxValueValidator(999999)])

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='kombo/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp'])])
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Kombo'
        verbose_name = 'kombo'
        verbose_name_plural = 'kombo'

    def save(self, *args, **kwargs):
        self.category = Category.objects.get(name='kombo')
        super(Kombo, self).save(*args, **kwargs)


class ChildKombo(BaseModel):
    CHILD_STATUS = (
        ('belister', 'belister'),
        ('zakuska', 'zakuska'),
        ('napitok', 'napitok'),
        ('pitsa', 'pitsa'),
        ('disert', 'disert')
    )

    status = models.CharField(max_length=20, choices=CHILD_STATUS)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(20)])

    product = models.ManyToManyField(Product, through='ChildKomboItem')
    kombo = models.ForeignKey(Kombo, on_delete=models.CASCADE, related_name='kombochild')

    def __str__(self):
        return f"{self.kombo} | {self.status}"

    class Meta:
        db_table = 'ChildKombo'
        verbose_name = 'kombo child'
        verbose_name_plural = 'kombo child'


class ChildKomboItem(models.Model):
    PIZZA_SIZE = (
        ('KICHKINA', 'KICHKINA'),
        ("O'RTACHA", "O'RTACHA"),
        ('KATTA', 'KATTA')
    )

    childkombo = models.ForeignKey(ChildKombo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    is_pizza = models.BooleanField(default=False)
    overprice = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], blank=True, null=True)
    size = models.CharField(max_length=10, choices=PIZZA_SIZE, blank=True, null=True)

    def __str__(self):
        return f"{self.childkombo} ~ {self.product}"

    class Meta:
        db_table = 'ChildKomboItem'
        verbose_name = 'kombo child item'
        verbose_name_plural = 'kombo child items'
