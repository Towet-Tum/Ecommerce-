# Generated by Django 5.1.6 on 2025-02-15 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_id',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('base_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='orders_ship_name_73b0b5_idx')],
            },
        ),
        migrations.CreateModel(
            name='OrderShipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_method', models.CharField(max_length=100)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('shipped_date', models.DateTimeField(blank=True, null=True)),
                ('estimated_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='orders.order')),
            ],
            options={
                'indexes': [models.Index(fields=['order'], name='orders_orde_order_i_f2fefb_idx')],
            },
        ),
    ]
