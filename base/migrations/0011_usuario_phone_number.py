# Generated by Django 4.2.15 on 2024-09-02 02:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_pedido_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="El número de teléfono debe cumplir con el formato: '+999999999'. Solo se permiten números con 15 digitos.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
