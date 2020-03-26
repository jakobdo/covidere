from django.db import models
from django.conf import settings

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField()
    phone = models.CharField(max_length=20)
    mobilepay = models.CharField(max_length=8)
    contact = models.CharField(max_length=50)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)
