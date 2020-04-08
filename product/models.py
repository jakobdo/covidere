from django.db import models
from django.utils.translation import gettext_lazy


class ProductSize(models.Model):
    """
    Product Size model
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    """
    Product Color model
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model
    """
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    name = models.CharField(gettext_lazy('name'), max_length=100)
    description = models.TextField(gettext_lazy('description'))
    price = models.DecimalField(gettext_lazy('price'), max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(gettext_lazy('offer price'), max_digits=10, decimal_places=2, blank=True, null=True)
    size = models.ManyToManyField(ProductSize, blank=True)
    color = models.ManyToManyField(ProductColor, blank=True)
    image = models.ImageField(gettext_lazy('image'), upload_to='images/%Y/%m/%d/')

    active = models.BooleanField(gettext_lazy('active'), default=True)
    delivery_days = models.PositiveIntegerField(gettext_lazy('delivery days'), blank=True, null=True)
    start_datetime = models.DateTimeField(gettext_lazy('start datetime'), blank=True, null=True)
    end_datetime = models.DateTimeField(gettext_lazy('end datetime'), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
