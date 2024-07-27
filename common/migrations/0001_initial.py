# Generated by Django 5.0.6 on 2024-07-20 10:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=250)),
                ('bino_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='uy/bino raqami')),
                ('office_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='uy/office raqami')),
                ('podyezt', models.CharField(blank=True, max_length=10, null=True)),
                ('qavat', models.CharField(blank=True, max_length=10, null=True)),
                ('door_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='eshik raqami')),
                ('name_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='manzil nomi')),
                ('note_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='manzilga izoh')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
