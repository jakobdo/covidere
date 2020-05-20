from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from stdimage import JPEGField


class ActiveManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super().get_queryset()
            .filter(
                active=True,
                shop__active=True
            )
            .filter(
                Q(start_datetime__lte=now, end_datetime__gte=now) |
                Q(start_datetime__isnull=True, end_datetime__gte=now) |
                Q(start_datetime__lte=now, end_datetime__isnull=True) |
                Q(start_datetime__isnull=True, end_datetime__isnull=True)
            )
            .prefetch_related("shop")
        )


class InactiveManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super().get_queryset()
            .filter(
                shop__active=True
            )
            .filter(
                Q(active=False) |
                Q(start_datetime__gte=now) |
                Q(end_datetime__lte=now)
            )
            .prefetch_related("shop")
        )


class Product(models.Model):
    """
    Product model
    """
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    name = models.CharField(gettext_lazy('name'), max_length=100)
    description = models.TextField(gettext_lazy('description'))
    price = models.DecimalField(
        gettext_lazy('price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    offer_price = models.DecimalField(
        gettext_lazy('offer price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    image = JPEGField(
        gettext_lazy('image'),
        upload_to='images/%Y/%m/%d/',
        variations={'full': (600, 400, True)},
    )

    active = models.BooleanField(gettext_lazy('active'), default=True)
    start_datetime = models.DateTimeField(
        gettext_lazy('start datetime'),
        blank=True,
        null=True
    )
    end_datetime = models.DateTimeField(
        gettext_lazy('end datetime'),
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    actives = ActiveManager()
    inactives = InactiveManager()

    def __str__(self):
        return self.name

    def get_price(self):
        return self.offer_price if self.offer_price else self.price

        
