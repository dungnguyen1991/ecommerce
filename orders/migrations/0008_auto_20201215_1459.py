# Generated by Django 3.1.1 on 2020-12-15 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20201214_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpurchase',
            old_name='Order_id',
            new_name='order_id',
        ),
    ]
