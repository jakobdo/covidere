from django.conf import settings
from django.db import models
from django.utils.http import urlencode
from django.utils.text import slugify
from django.utils.translation import gettext_lazy


class Postcode(models.Model):
    postcode = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.postcode} - {self.city}"


class Shop(models.Model):
    name = models.CharField(gettext_lazy("name"), max_length=100)
    address = models.CharField(gettext_lazy("address"), max_length=100)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE, related_name="shops")
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
    delivery_postcode = models.ManyToManyField(Postcode, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def location(self):
        """
        Helper to provide the urlencoded information for a shop to google maps
        """
        data = dict(
            query=f"{self.name} {self.address} {self.postcode.postcode} {self.postcode.city}"
        )
        return urlencode(data)
    
    def slug(self):
        """
        Will convert shop.name to a slug
        """
        return slugify(f"{self.name} {self.pk}")
