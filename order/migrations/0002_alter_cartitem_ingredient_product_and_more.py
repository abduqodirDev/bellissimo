# Generated by Django 5.0.6 on 2024-07-24 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='ingredient_product',
            field=models.ManyToManyField(blank=True, help_text='faqat pizza va gazak uchun kiriting', to='product.ingredient'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, help_text="Kombo bo'lsa bo'sh qoldiring", null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(choices=[('PRODUCT', 'PRODUCT'), ('KOMBO', 'KOMBO'), ('PIZZA', 'PIZZA'), ('GAZAK', 'GAZAK')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
