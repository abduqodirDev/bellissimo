# Generated by Django 5.0.6 on 2024-07-17 08:08

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'category',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ingredient/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])),
                ('status', models.CharField(choices=[('PIZZA', 'PIZZA'), ('GAZAK', 'GAZAK')], max_length=20)),
                ('price_status', models.CharField(choices=[('SINGLE_PRICE', 'SINGLE_PRICE'), ('MULTI_PRICE', 'MULTI_PRICE')], max_length=20)),
                ('small_price', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('medium_price', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('big_price', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('in_stock', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredient',
                'db_table': 'Ingredient',
            },
        ),
        migrations.CreateModel(
            name='IngredientToProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('STANDART', 'STANDART'), ('MIKS', 'MIKS'), ('SINGLE', 'SINGLE'), ('GAZAK', 'GAZAK')], max_length=20, null=True, unique=True)),
                ('ingredient', models.ManyToManyField(to='product.ingredient')),
            ],
            options={
                'verbose_name': 'IngredientToProduct',
                'verbose_name_plural': 'IngredientToProduct',
                'db_table': 'IngredientToProduct',
            },
        ),
        migrations.CreateModel(
            name='ProductChild',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PIZZA', 'PIZZA'), ('GAZAK', 'GAZAK')], max_length=20)),
                ('pizza_type', models.CharField(blank=True, choices=[('STANDART', 'STANDART'), ('MIKS', 'MIKS'), ('SINGLE', 'SINGLE')], help_text="agar mahsulot gazak turiga kirsa bu o'rinni bo'sh qoldirib keting", max_length=20, null=True)),
                ('price_small_pizza', models.PositiveIntegerField(blank=True, help_text='faqat standart pitsa uchun', null=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('price_medium_pizza', models.PositiveIntegerField(blank=True, help_text='faqat standart pitsa uchun', null=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('price_big_pizza', models.PositiveIntegerField(blank=True, help_text='faqat standart pitsa uchun', null=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('ingredient_count', models.CharField(blank=True, choices=[('1', '1'), ('10', '10'), ('40', '40')], help_text='faqat pitsa uchun kiritiladi', max_length=3, null=True)),
                ('ingredient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ingredienttoproduct')),
            ],
            options={
                'verbose_name': 'ProductChild',
                'verbose_name_plural': 'ProductChild',
                'db_table': 'ProductChild',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PITSA', 'PITSA'), ('GAZAK', 'GAZAK'), ('PRODUCT', 'PRODUCT')], default='PRODUCT', max_length=20)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('price', models.PositiveIntegerField(blank=True, help_text="agar mahsulotingiz pitsa bo'lib standart turiga kirsa narx kiritilmaydi", null=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('image', models.ImageField(upload_to='product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'png', 'webp'))])),
                ('in_stock', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product.category')),
                ('product_child', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productchild')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'product',
                'db_table': 'Product',
            },
        ),
    ]