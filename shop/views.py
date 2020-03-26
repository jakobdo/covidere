from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from shop.models import Shop


class ShopView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print(self.request)
        shop = self.request.user.shop
        context = {'shop': shop}
        return render(request, 'shop/overview.html', context)


class ShopDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print(self.request)
        shop = self.request.user.shop
        context = {'shop': shop}
        return render(request, 'shop/overview.html', context)