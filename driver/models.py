from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy

from shop.models import Postcode


class Driver(models.Model):
    name = models.CharField(gettext_lazy("driver name"), max_length=100)
    address = models.CharField(gettext_lazy("address"), max_length=100)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE, related_name="drivers")
    homepage = models.URLField(gettext_lazy("homepage"))
    email = models.EmailField(gettext_lazy("contact email"))
    phone = models.CharField(gettext_lazy("phone"), max_length=20)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(gettext_lazy("active"), default=False)
    delivery_postcode = models.ManyToManyField(Postcode, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
