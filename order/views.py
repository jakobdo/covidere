from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from order.forms import OrderForm
from order.models import Order


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order/create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_thanks')


class OrderCreatedView(TemplateView):
    template_name = 'order/thanks.html'

    def get(self, request, *args, **kwargs):
        del request.session['basket']
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
