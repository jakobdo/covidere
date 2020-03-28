from django.db import models
from django.conf import settings

class Zipcode(models.Model):
    zipcode = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.zipcode} - {self.name}"


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.ForeignKey(Zipcode, on_delete=models.CASCADE, related_name="shops")
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
    deliver = models.BooleanField(default=True)
    delivery_zipcode = models.ManyToManyField(Zipcode, blank=True)

    def __str__(self):
        return self.name