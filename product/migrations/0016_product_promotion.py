# Generated by Django 3.2.6 on 2021-11-06 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_remove_product_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='promotion',
            field=models.DecimalField(decimal_places=0, max_digits=12, null=True),
        ),
    ]
