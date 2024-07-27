from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.db import models

from common.models import BaseModel


STANDART, MIKS, SINGLE, GAZAK = ("STANDART", "MIKS", "SINGLE", "GAZAK")
PIZZA, GAZAK = ("PIZZA", "GAZAK")
SINGLE_PRICE, MULTI_PRICE = ("SINGLE_PRICE", "MULTI_PRICE")


class Category(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'
        verbose_name = 'category'
        verbose_name_plural = 'category'


class Product(BaseModel):
    PRODUCT_STATUS = (
        ('PITSA', 'PITSA'),
        ('GAZAK', 'GAZAK'),
        ('PRODUCT', 'PRODUCT')
    )

    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='PRODUCT')
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999999)], blank=True, null=True,
                                        help_text='agar mahsulotingiz pitsa bo\'lib standart turiga kirsa narx kiritilmaydi')
    image = models.ImageField(upload_to='product/',
                              validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'png', 'webp'))])

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    product_child = models.OneToOneField('ProductChild', on_delete=models.SET_NULL, null=True, blank=True)

    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category} | {self.name}"

    class Meta:
        db_table = 'Product'
        verbose_name = 'product'
        verbose_name_plural = 'product'

    def clean(self):
        cate_pitsa = Category.objects.get(name="pitsa")
        cate_gazak = Category.objects.get(name="gazaklar")
        if self.status == "PITSA":
            if self.category != cate_pitsa:
                raise ValidationError("Categoriyani xato kiritdingiz!!!")
        elif self.status == GAZAK:
            if self.category != cate_gazak:
                raise ValidationError("Categoriyani xato kiritdingiz!!!")
        else:
            if self.category == cate_pitsa or self.category == cate_gazak:
                raise ValidationError("Categoriyani xato kiritdingiz!!!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ProductChild(BaseModel):
    PRODUCT_STATUS = (
        ('PIZZA', 'PIZZA'),
        ('GAZAK', 'GAZAK')
    )
    PIZZA_TYPE = (
        ('STANDART', 'STANDART'),
        ('MIKS', 'MIKS'),
        ('SINGLE', 'SINGLE')
    )
    INGREDIENT_TYPE = (
        ('1', '1'),
        ('10', '10'),
        ('40', '40')
    )

    status = models.CharField(max_length=20, choices=PRODUCT_STATUS)
    pizza_type = models.CharField(max_length=20, choices=PIZZA_TYPE, blank=True, null=True,
                                  help_text='agar mahsulot gazak turiga kirsa bu o\'rinni bo\'sh qoldirib keting')
    price_small_pizza = models.PositiveIntegerField(validators=[MaxValueValidator(999999)], blank=True, null=True,
                                                    help_text="faqat standart pitsa uchun")
    price_medium_pizza = models.PositiveIntegerField(validators=[MaxValueValidator(999999)], blank=True, null=True,
                                                    help_text="faqat standart pitsa uchun")
    price_big_pizza = models.PositiveIntegerField(validators=[MaxValueValidator(999999)], blank=True, null=True,
                                                    help_text="faqat standart pitsa uchun")
    ingredient_count = models.CharField(max_length=3, choices=INGREDIENT_TYPE, blank=True, null=True,
                                        help_text="faqat pitsa uchun kiritiladi")
    ingredient = models.ForeignKey('IngredientToProduct', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.status == GAZAK:
            just = f"{self.status} ~ {self.id}"
        else:
            just = f"{self.status} - {self.pizza_type} ~ {self.id}"
        return just

    class Meta:
        db_table = 'ProductChild'
        verbose_name = 'ProductChild'
        verbose_name_plural = 'ProductChild'

    def clean(self):
        if self.status == GAZAK and (self.pizza_type or self.price_small_pizza or
                                       self.price_medium_pizza or self.price_big_pizza):
            raise ValidationError("Mahsuotingiz 'GAZAK' turkumiga kirsa qolgan fieldlar bo'sh bo'lishi kerak!!!")

        if ((self.pizza_type == SINGLE and self.ingredient_count != '1') or
                (self.pizza_type == MIKS and self.ingredient_count != '10') or
                (self.pizza_type == STANDART and self.ingredient_count != '40')):
            raise ValidationError("Masalliqlar sonini xato kiritdingiz!!!")

        if self.status == PIZZA:
            standart = IngredientToProduct.objects.get(status=STANDART)
            miks = IngredientToProduct.objects.get(status=MIKS)
            single = IngredientToProduct.objects.get(status=SINGLE)
            if ((self.pizza_type == STANDART and self.ingredient != standart) or
                    (self.pizza_type == MIKS and self.ingredient != miks) or
                    (self.pizza_type == SINGLE and self.ingredient != single)):
                raise ValidationError("Ingredient xato kiritildi!!!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    INGREDIENT_TYPE = (
        ('PIZZA', 'PIZZA'),
        ('GAZAK', 'GAZAK')
    )
    PRICE_TYPE = (
        ('SINGLE_PRICE', 'SINGLE_PRICE'),
        ('MULTI_PRICE', 'MULTI_PRICE')
    )

    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='ingredient/', null=True, blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    status = models.CharField(max_length=20, choices=INGREDIENT_TYPE)
    price_status = models.CharField(max_length=20, choices=PRICE_TYPE)
    small_price = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], blank=True, null=True)
    medium_price = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], blank=True, null=True)
    big_price = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], blank=True, null=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ~ {self.status}"

    class Meta:
        db_table = 'Ingredient'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredient'

    def clean(self):
        if self.status == PIZZA:
            if self.price_status != MULTI_PRICE or not self.small_price or not self.medium_price or not self.big_price:
                raise ValidationError("Qatorlar bo'sh bo'lmasligi zarur!!!")
        else:
            if self.price_status!=SINGLE_PRICE or self.small_price or self.medium_price or self.big_price:
                raise ValidationError("masalliq 'GAZAK' bo'lsa qolgan fieldlar bo'sh qoladi!!!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class IngredientToProduct(models.Model):
    STATUS = (
        ('STANDART', 'STANDART'),
        ('MIKS', 'MIKS'),
        ('SINGLE', 'SINGLE'),
        ('GAZAK', 'GAZAK')
    )

    ingredient = models.ManyToManyField(Ingredient)
    status = models.CharField(max_length=20, choices=STATUS, unique=True, null=True, blank=True)

    def __str__(self):
        if self.status == STANDART:
            return f"ITP Standart"
        elif self.status == MIKS:
            return f"ITP MIKS"
        elif self.status == SINGLE:
            return f"ITP SINGLE"
        else:
            return f"ITP GAZAK"

    class Meta:
        db_table = 'IngredientToProduct'
        verbose_name = 'IngredientToProduct'
        verbose_name_plural = 'IngredientToProduct'
