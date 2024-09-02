# Generated by Django 4.2.15 on 2024-08-29 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_usuario_alter_item_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entregado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.usuario')),
            ],
        ),
    ]
