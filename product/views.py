from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView

from product.models import Product
from shop.models import Postcode, Shop


class IndexView(ListView):
    model = Product
    template_name = 'product/index.html'

    def get(self, request, *args, **kwargs):
        response = super(IndexView, self).get(request, *args, **kwargs)
        # Do we have a postcode from a cookie or session?
        cookie_postcode = request.COOKIES.get('postcode', False)
        session_postcode = request.session.get('postcode', False)
        if cookie_postcode and not session_postcode:
            try:
                postcode = Postcode.objects.get(postcode=cookie_postcode)
                request.session['postcode'] = postcode.postcode
            except Postcode.DoesNotExist:
                return redirect('postcode_index')
        return response

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
            .order_by('?')
        )
        shop_pk = self.kwargs.get('pk')
        if shop_pk:
            shop = get_object_or_404(Shop, pk=shop_pk, active=True)
            queryset = queryset.filter(shop=shop)
        # TODO - Add postcode stuff if needed ?
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
