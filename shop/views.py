from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from order.models import Order
from product.models import Product
from shop.models import Shop


class ShopIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/overview.html'


class ShopUpdateView(UpdateView):
    model = Shop
    fields = ['name', 'address', 'zipcode', 'city', 'email', 'homepage', 'phone', 'mobilepay', 'contact']
    template_name = 'shop/update.html'
    success_url = reverse_lazy('shop_updated')

    def get_object(self, queryset=None):
        return self.request.user.shop


class ShopUpdatedView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/updated.html'


class ShopProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(shop=self.request.user.shop)
        return queryset

class ShopOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(shop=self.request.user.shop)
        return queryset


class ShopOverviewView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shop/overview.html')