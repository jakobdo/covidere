from django.db import models

class ProductSize(models.Model):
    name = models.CharField(max_length=100)


class ProductColor(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # TODO
    # Price on sale
    # Regular price
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ManyToManyField(ProductSize, blank=True)
    color = models.ManyToManyField(ProductColor, blank=True)

    active = models.BooleanField(default=True)
    delivery_days = models.PositiveIntegerField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
