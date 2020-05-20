from django.contrib.gis.db.models.functions import GeometryDistance
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from product.models import Product
from postcode.models import Postcode
from shop.models import Shop


class ProductsView(ListView):
    model = Product
    template_name = 'product/index.html'

    def get_queryset(self):
        limitation = True
        queryset = self.model.actives.order_by('?')
        shop_pk = self.kwargs.get('pk')
        if shop_pk:
            limitation = False
            shop = get_object_or_404(Shop, pk=shop_pk, active=True)
            queryset = queryset.filter(shop=shop)

        query = self.request.GET.get('q')
        if query:
            limitation = False
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if limitation:
            queryset = queryset[:12]
        return queryset


class ProductsNewestView(ListView):
    model = Product
    template_name = 'product/newest.html'

    def get_queryset(self):
        return self.model.actives.order_by('created')


class ProductsOfferView(ListView):
    model = Product
    template_name = 'product/offer.html'

    def get_queryset(self):
        queryset = self.model.actives.order_by('?')
        return queryset.filter(offer_price__isnull=False)


class ProductsPostcodeView(ListView):
    model = Product
    template_name = 'product/postcode.html'

    def get_queryset(self):
        postcode = self.kwargs.get('postcode')
        postcode = get_object_or_404(Postcode, postcode=postcode, active=True)
        return self.model.actives.order_by(GeometryDistance("shop__location", postcode.location))
