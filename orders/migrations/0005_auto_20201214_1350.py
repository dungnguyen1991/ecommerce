# Generated by Django 3.1.1 on 2020-12-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20201204_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address_final',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_final',
            field=models.TextField(blank=True, null=True),
        ),
    ]
