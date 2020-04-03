from django.conf import settings
from django.db import models
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy


class Zipcode(models.Model):
    zipcode = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.zipcode} - {self.name}"


class Shop(models.Model):
    name = models.CharField(gettext_lazy("name"), max_length=100)
    address = models.CharField(gettext_lazy("address"), max_length=100)
    zipcode = models.ForeignKey(Zipcode, on_delete=models.CASCADE, related_name="shops")
    city = models.CharField(gettext_lazy("city"), max_length=100)
    email = models.EmailField(gettext_lazy("email"))
    homepage = models.URLField(gettext_lazy("homepage"))
    phone = models.CharField(gettext_lazy("phone"), max_length=20)
    mobilepay = models.CharField(gettext_lazy("mobilepay"), max_length=8)
    contact = models.CharField(gettext_lazy("contact"), max_length=50)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(gettext_lazy("active"), default=True)
    deliver = models.BooleanField(gettext_lazy("deliver"), default=True)
    delivery_zipcode = models.ManyToManyField(Zipcode, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def location(self):
        """
        Helper to provide the urlencoded information for a shop to google maps
        """
        data = dict(
            query=f"{self.name} {self.address} {self.zipcode} {self.city}"
        )
        return urlencode(data)
