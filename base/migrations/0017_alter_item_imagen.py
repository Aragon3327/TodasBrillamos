# Generated by Django 4.2.15 on 2024-09-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_item_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='items'),
        ),
    ]
