from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from shop.models import Shop


class ShopListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Shop List View. Will list all shops.
    """
    permission_required = 'base.alten_admin'
    model = Shop
    template_name = 'shop/alten/list.html'

    def get_queryset(self):
        queryset = Shop.objects.filter(active=False).order_by('name')
        return queryset


class ShopDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Shop Detail View. Will show detail for a given shop.
    """
    permission_required = 'base.alten_admin'
    model = Shop
    template_name = 'shop/alten/detail.html'

    def get_queryset(self):
        queryset = Shop.objects.filter(active=False).order_by('name')
        return queryset


class ShopActivateView(View):
    def get(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk, active=False)
        shop.active = True
        shop.save()
        return redirect('alten_shop_list')
