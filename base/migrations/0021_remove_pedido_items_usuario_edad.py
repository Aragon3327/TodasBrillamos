# Generated by Django 4.2.15 on 2024-10-02 02:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_item_descuento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='items',
        ),
        migrations.AddField(
            model_name='usuario',
            name='edad',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
