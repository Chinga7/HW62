# Generated by Django 4.1.3 on 2023-01-10 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=100, verbose_name='Client')),
                ('contact_number', models.CharField(max_length=100, verbose_name='Contact Number')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Order Date Creation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Description')),
                ('category', models.TextField(choices=[('other', 'Other'), ('books', 'Books'), ('flowers', 'Flowers'), ('furniture', 'Furniture'), ('gadgets', 'Gadgets')], default='other', max_length=30, verbose_name='Status')),
                ('leftover', models.IntegerField(verbose_name='Left Over')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Price')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Product Date Creation')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='webapp.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='webapp.product', verbose_name='Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='order', through='webapp.ProductOrder', to='webapp.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
