from django.contrib.gis.db.models.functions import GeometryDistance
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from product.models import Product
from shop.models import Postcode, Shop


class ProductsView(ListView):
    model = Product
    template_name = 'product/index.html'

    def get_queryset(self):
        queryset = self.model.actives.order_by('?')
        shop_pk = self.kwargs.get('pk')
        if shop_pk:
            shop = get_object_or_404(Shop, pk=shop_pk, active=True)
            queryset = queryset.filter(shop=shop)
        else:
            # Do we have a postcode from session?
            code = self.request.session.get('postcode')
            if code:
                try:
                    postcode = Postcode.objects.get(postcode=code)
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
        return self.model.actives.order_by('created')


class ProductsOfferView(ListView):
    model = Product
    template_name = 'product/offer.html'

    def get_queryset(self):
        queryset = self.model.actives.order_by('?')
        return queryset.filter(offer_price__isnull=False)
