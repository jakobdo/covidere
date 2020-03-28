from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from basket.forms import BasketAddForm


class Basket:
    def __init__(self, session):
        self.session = session
    
    def add(self, product, color, size):
        # Add or update item
        basket = self.session.setdefault('basket', [])
        item = next((item for item in basket if (item['product'] == product and item['color'] == color and item['size'] == size)), None)
        if item:
            item['count'] += 1
        else:
            basket.append(dict(
                product=product,
                color=color,
                size=size,
                count=1
            ))
        return basket

class BasketAddView(FormView):
    template_name = 'basket/add.html'
    form_class = BasketAddForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        basket = Basket(self.request.session)
        self.request.session['basket'] = basket.add(
            form.cleaned_data.get('product'),
            form.cleaned_data.get('color'),
            form.cleaned_data.get('size'),
        )
        self.request.session.modified = True
        return super().form_valid(form)


class BasketIndexView(TemplateView):
    template_name = "basket/list.html"

    def get_context_data(self, **kwargs):
        context = super(BasketIndexView, self).get_context_data(**kwargs)
        context['basket'] = self.request.session.get('basket', [])
        return context
