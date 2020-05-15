from django.db import models
from django.utils.translation import gettext_lazy

from postcode.models import Postcode


class Order(models.Model):
    ORDERED = 1
    ACCEPTED = 2
    SENT = 3
    REJECTED = 4

    ORDER_STATUS_CHOICES = [
        (ORDERED, gettext_lazy('Ordered')),
        (ACCEPTED, gettext_lazy('Accepted')),
        (SENT, gettext_lazy('Sent')),
        (REJECTED, gettext_lazy('Rejected')),
    ]
    name = models.CharField(gettext_lazy('name'), max_length=100)
    address = models.CharField(gettext_lazy('address'), max_length=100)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE, related_name="orders")
    email = models.EmailField(gettext_lazy('email'))
    mobile = models.CharField(gettext_lazy('mobile'), max_length=20)
    status = models.IntegerField(
        gettext_lazy('status'),
        choices=ORDER_STATUS_CHOICES,
        default=ORDERED
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.count * self.price
