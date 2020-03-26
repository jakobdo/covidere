from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone

from product.models import Product


class IndexView(ListView):
    model = Product
    template_name = 'index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        # Find all products where start and end are NOW
        # Find all products that are active
        now = timezone.now()
        queryset = queryset.filter(start_datetime__lte=now, end_datetime__gte=now)
        return queryset
