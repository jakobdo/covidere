from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, TemplateView, UpdateView

from shop.models import Shop


class ShopIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/overview.html'


class ShopDetail(LoginRequiredMixin, UpdateView):
    model = Shop