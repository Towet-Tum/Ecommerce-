# Generated by Django 5.1.6 on 2025-02-15 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('orders', '0003_alter_order_user_id'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='orderitem',
            new_name='orders_orde_product_5c1733_idx',
            old_name='orders_orde_product_c4062e_idx',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_variant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='catalog.productvariant'),
        ),
        migrations.AlterField(
            model_name='ordershipment',
            name='shipping_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.shippingmethod'),
        ),
    ]
