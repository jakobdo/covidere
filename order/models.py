from django.db import models


class Order(models.Model):
    ORDERED = 1
    ACCEPTED = 2
    SENT = 3
    REJECTED = 4
    
    ORDER_STATUS_CHOICES = [
        (ORDERED, 'Bestilt'),
        (ACCEPTED, 'Accepteret'),
        (SENT, 'Afsendt'),
        (REJECTED, 'Afvist'),
    ]
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=ORDERED)


class OrderItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    color = models.ForeignKey('product.ProductColor', blank=True, null=True, on_delete=models.CASCADE)
    size = models.ForeignKey('product.ProductSize', blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
