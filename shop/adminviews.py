import datetime
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from order.models import Order
from product.models import Product
from shop.forms import OrderStatusForm, ShopProductForm
from shop.models import Shop


class ShopUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Shop Update View, handle view and update shop objects. Will only allow update of users own shop for now
    """
    model = Shop
    fields = ['name', 'address', 'postcode', 'email', 'homepage', 'phone', 'order_pickup', 'delivery_range',]
    template_name = 'shop/update.html'
    success_url = reverse_lazy('shop_update')
    success_message = "Information updated!"

    def get_form(self, form_class=None):
        form = super(ShopUpdateView, self).get_form(form_class)
        form.fields['postcode'].required = True
        return form

    def get_object(self, queryset=None):
        return self.request.user.shop


class ShopProductActiveListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/active_product_list.html'

    def get_queryset(self):
        return self.model.actives.filter(shop=self.request.user.shop)


class ShopProductInactiveListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/inactive_product_list.html'

    def get_queryset(self):
        queryset = Product.inactives.filter(shop=self.request.user.shop)
        return queryset


class ShopProductExpiringListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/expiring_product_list.html'

    def get_queryset(self):
        now = timezone.now()
        one_week_from_now = now + timedelta(days=7)
        queryset = Product.actives.filter(end_datetime__gte=now, end_datetime__lte=one_week_from_now, shop=self.request.user.shop)
        return queryset


class ShopProductListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(shop=self.request.user.shop)
        return queryset


class ShopOrderListView(LoginRequiredMixin, ListView):
    """
    Shop Order List View. Will list all orders related to a shop. 
    For now based on current user. 
    Orders can contains products from other shops.
    """
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(items__product__shop=self.request.user.shop).distinct()
        return queryset


class ShopNewOrderListView(LoginRequiredMixin, ListView):
    """
    Shop Order List View. Will list all new orders related to a shop. 
    For now based on current user. 
    Orders can contains products from other shops.
    """
    model = Order
    template_name = 'shop/order_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(items__product__shop=self.request.user.shop, status=Order.ORDERED).distinct()
        return queryset


class ShopOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.filter(product__shop=self.request.user.shop).select_related('product').order_by('product__name')
        total = 0
        for item in items:
            total += item.subtotal()
        context['items'] = items
        context['total'] = total
        context['order'] = Order
        context['form'] = OrderStatusForm(instance=self.object)
        return context
    
    def get_queryset(self):
        queryset = Order.objects.filter(items__product__shop=self.request.user.shop).distinct()
        return queryset
    

class ShopOrderStatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderStatusForm
    success_message = gettext_lazy("Status updated")

    def get_queryset(self):
        queryset = Order.objects.filter(items__product__shop=self.request.user.shop).distinct()
        return queryset

    def get_success_url(self):
        return reverse('show_order_detail', kwargs={'pk': self.object.pk})


class ShopOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.request.user.shop

        now = timezone.now()
        in_a_week = now + datetime.timedelta(days=7)

        context['shop'] = shop
        context['counts'] = dict(
            new_orders=Order.objects.filter(items__product__shop=shop, status=Order.ORDERED).distinct().count(),
            active_products=Product.actives.filter(shop=shop).count(),
            expiring_products=Product.objects.filter(shop=shop, active=True, start_datetime__lte=now, end_datetime__gte=now, end_datetime__lte=in_a_week).count(),
            inactive_products=Product.inactives.filter(shop=shop).count(),
        )
        return context


class ShopProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ShopProductForm
    template_name = 'product/update.html'
    success_url = reverse_lazy('shop_products')

    def get_form_kwargs(self):
        kw = super(ShopProductUpdateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_queryset(self):
        queryset = Product.objects.filter(shop=self.request.user.shop)
        return queryset


class ShopProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ShopProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('shop_products')

    def get_form_kwargs(self):
        kw = super(ShopProductCreateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.shop = self.request.user.shop
        return super(ShopProductCreateView, self).form_valid(form)
