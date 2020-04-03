from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone

from product.models import Product


class IndexView(ListView):
    model = Product
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        now = timezone.now()
        # Only show active products, from active shops and in "active" timespan!
        queryset = (
            queryset
            .filter(active=True)
            .filter(shop__active=True)
            .filter(start_datetime__lte=now, end_datetime__gte=now)
        ).prefetch_related("size").prefetch_related("color").prefetch_related("shop")
        return queryset
