# Generated by Django 3.2.6 on 2021-11-06 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_images1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]