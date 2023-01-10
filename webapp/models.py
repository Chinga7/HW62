from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('other', 'Other'),
        ('books', 'Books'),
        ('flowers', 'Flowers'),
        ('furniture', 'Furniture'),
        ('gadgets', 'Gadgets')
    ]

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Name')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    category = models.TextField(choices=CATEGORY_CHOICES, default='other', max_length=30, null=False, blank=False, verbose_name='Status')
    leftover = models.IntegerField(verbose_name='Left Over')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Price')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Product Date Creation')

    def get_absolute_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.pk})


class Order(models.Model):
    class Meta:
        ordering = ['-created_at']

    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='orders', verbose_name="User")
    product = models.ManyToManyField('webapp.Product', related_name='order', through='webapp.ProductOrder',
                                     through_fields=('order', 'product'), blank=True)
    client = models.CharField(max_length=100, null=False, blank=False, verbose_name='Client')
    contact_number = models.CharField(max_length=100, null=False, blank=False, verbose_name='Contact Number')
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name='Address')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Order Date Creation')

    def __str__(self):
        return f'{self.pk}. {self.client}. {self.contact_number}. {self.created_at}'


class ProductOrder(models.Model):
    order = models.ForeignKey('webapp.Order', related_name='order_product', on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey('webapp.Product', related_name='product_order', on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Quantity')
