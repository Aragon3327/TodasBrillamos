# Generated by Django 4.2.15 on 2024-08-29 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_usuario_nombre_alter_usuario_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
