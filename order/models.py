from django.db import models


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    color = models.ForeignKey('product.ProductColor', blank=True, null=True, on_delete=models.CASCADE)
    size = models.ForeignKey('product.ProductSize', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
