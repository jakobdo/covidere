import requests
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.http import urlencode
from django.utils.text import slugify
from django.utils.translation import gettext_lazy
from phonenumber_field.modelfields import PhoneNumberField

from postcode.models import Postcode


class Shop(models.Model):
    name = models.CharField(gettext_lazy("shop name"), max_length=100)
    address = models.CharField(gettext_lazy("address"), max_length=100)
    postcode = models.ForeignKey(Postcode, on_delete=models.CASCADE, related_name="shops", blank=True, null=True)
    homepage = models.URLField(gettext_lazy("homepage"))
    email = models.EmailField(gettext_lazy("contact email"))
    phone = PhoneNumberField(gettext_lazy("phone"), max_length=17, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(gettext_lazy("active"), default=False)
    delivery_postcode = models.ManyToManyField(Postcode, blank=True)

    # Internal used fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    location = models.PointField(blank=True, null=True)

    def __str__(self):
        return self.name

    def map_query(self):
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
    
    def save(self, *args, **kwargs):
        if self.active and not self.location:
            # Fetch location from api!
            osm_url = 'https://nominatim.openstreetmap.org/search'
            query = dict(
                street=self.address,
                city=self.postcode.city,
                country="dk",
                postalcode=self.postcode.postcode,
                format="geojson"
            )
            full_url = f"{osm_url}?{urlencode(query)}"
            res = requests.get(full_url)
            coordinates = res.json().get('features')[0].get('geometry').get('coordinates')
            pnt = Point(coordinates)
            self.location = pnt
        super(Shop, self).save(*args, **kwargs)
