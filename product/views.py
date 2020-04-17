import tldextract
from django.contrib.gis.db.models.functions import GeometryDistance
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from product.models import Product
from shop.models import Postcode, Shop


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
            .filter(
                Q(start_datetime__lte=now, end_datetime__gte=now) | 
                Q(start_datetime__isnull=True, end_datetime__gte=now) | 
                Q(start_datetime__lte=now, end_datetime__isnull=True) |
                Q(start_datetime__isnull=True, end_datetime__isnull=True)
            )
            .prefetch_related("size")
            .prefetch_related("color")
            .prefetch_related("shop")
            .order_by('?')
        )
        shop_pk = self.kwargs.get('pk')
        if shop_pk:
            shop = get_object_or_404(Shop, pk=shop_pk, active=True)
            queryset = queryset.filter(shop=shop)
        else:
            # Do we have a postcode from the url?
            url = self.request.build_absolute_uri()
            ext = tldextract.extract(url)
            if ext.subdomain:
                try:
                    postcode = Postcode.objects.get(postcode=ext.subdomain)
                    queryset = queryset.order_by(GeometryDistance("shop__location", postcode.location))
                except Postcode.DoesNotExist:
                    queryset = queryset.order_by('?')
            else:
                queryset = queryset.order_by('?')

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


class ProductsOfferView(ListView):
    model = Product
    template_name = 'product/offer.html'

    def get_queryset(self):
        queryset = super().get_queryset()
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
