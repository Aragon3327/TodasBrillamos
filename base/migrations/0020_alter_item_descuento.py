# Generated by Django 4.2.15 on 2024-09-20 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_item_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='descuento',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
