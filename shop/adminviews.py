import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from order.models import Order
from product.models import Product
from shop.forms import ShopProductForm
from shop.models import Shop


class ShopUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Shop Update View, handle view and update shop objects. Will only allow update of users own shop for now
    """
    model = Shop
    fields = ['name', 'address', 'zipcode', 'city', 'email', 'homepage', 'phone', 'mobilepay', 'contact']
    template_name = 'shop/update.html'
    success_url = reverse_lazy('shop_update')
    success_message = "Information updated!"

    def get_object(self, queryset=None):
        return self.request.user.shop


class ShopProductActiveListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/active_product_list.html'

    def get_queryset(self):
        now = timezone.now()
        queryset = Product.objects.filter(shop=self.request.user.shop, active=True, start_datetime__lte=now, end_datetime__gte=now)
        return queryset


class ShopProductInactiveListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/inactive_product_list.html'

    def get_queryset(self):
        now = timezone.now()
        queryset = Product.objects.filter(Q(start_datetime__gte=now) | Q(end_datetime__lte=now) | Q(active=False), shop=self.request.user.shop)
        return queryset


class ShopProductExpiringListView(LoginRequiredMixin, ListView):
    """
    Shop Product List View. Will list all products related to a single shop. Based on current user.
    """
    model = Product
    template_name = 'shop/expiring_product_list.html'

    def get_queryset(self):
        now = timezone.now()
        queryset = Product.objects.filter(Q(start_datetime__gte=now) | Q(end_datetime__lte=now) | Q(active=False), shop=self.request.user.shop)
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
            active_products=Product.objects.filter(shop=shop, active=True, start_datetime__lte=now, end_datetime__gte=now).count(),
            expiring_products=Product.objects.filter(shop=shop, active=True, start_datetime__lte=now, end_datetime__gte=now, end_datetime__lte=in_a_week).count(),
            inactive_products=Product.objects.filter(Q(start_datetime__gte=now) | Q(end_datetime__lte=now) | Q(active=False), shop=shop).count(),
        )
        return context


class ShopProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    #fields = ['name', 'description', 'image', 'price', 'offer_price', 'color', 'size', 'active', 'delivery_days', 'start_datetime', 'end_datetime']
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
