# Generated by Django 4.2.15 on 2024-09-02 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_usuario_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='items',
            field=models.ManyToManyField(related_name='items', to='base.item'),
        ),
    ]
