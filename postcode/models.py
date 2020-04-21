from django.contrib.gis.db import models


class Postcode(models.Model):
    postcode = models.PositiveSmallIntegerField(unique=True)
    city = models.CharField(max_length=100)
    location = models.PointField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['postcode']

    def __str__(self):
        return f"{self.postcode} - {self.city}"
