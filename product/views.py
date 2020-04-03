from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q

from product.models import Product


class IndexView(ListView):
    model = Product
    template_name = 'product/index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        now = timezone.now()
        # Only show active products, from active shops and in "active" timespan!
        queryset = (
            queryset
            .filter(active=True)
            .filter(shop__active=True)
            .filter(start_datetime__lte=now, end_datetime__gte=now)
            .prefetch_related("size")
            .prefetch_related("color")
            .prefetch_related("shop")
            .order_by('?')  # TODO - Queries may be expensive and slow
        )
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset


class ProductsNewestView(ListView):
    model = Product
    template_name = 'product/newest.html'

    def get_queryset(self):
        queryset = super(ProductsNewestView, self).get_queryset()
        now = timezone.now()
        # Only show active products, from active shops and in "active" timespan!
        queryset = (
            queryset
            .filter(active=True)
            .filter(shop__active=True)
            .filter(start_datetime__lte=now, end_datetime__gte=now)
            .prefetch_related("size")
            .prefetch_related("color")
            .prefetch_related("shop")
            .order_by('created')
        )
        return queryset


class ProductsOnSaleView(ListView):
    model = Product
    template_name = 'product/on_sale.html'

    def get_queryset(self):
        queryset = super(ProductsOnSaleView, self).get_queryset()
        now = timezone.now()
        # Only show active products, from active shops and in "active" timespan!
        queryset = (
            queryset
            .filter(active=True)
            .filter(shop__active=True)
            .filter(start_datetime__lte=now, end_datetime__gte=now)
            .prefetch_related("size")
            .prefetch_related("color")
            .prefetch_related("shop")
            .order_by('?')  # TODO - Queries may be expensive and slow
        )
        return queryset
