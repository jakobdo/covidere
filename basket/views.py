from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from basket.forms import BasketAddForm
from product.models import Product, ProductColor, ProductSize


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
        basket = self.request.session.get('basket', [])
        
        # Load products
        products = {p.id: p for p in Product.objects.filter(pk__in=[item.get('product') for item in basket]).select_related('shop')}
        # Load sizes
        sizes = {s.id: s.name for s in ProductSize.objects.filter(pk__in=[item.get('size') for item in basket])}
        # Load colors
        colors = {c.id: c.name for c in ProductColor.objects.filter(pk__in=[item.get('color') for item in basket])}

        new_basket = []

        for item in basket:
            count = item.get('count')
            price = products.get(item.get('product')).price
            new_item = dict(
                product_id=item.get('product'),
                product=products.get(item.get('product')).name,
                shop=products.get(item.get('product')).shop.name,
                size_id=item.get('size'),
                size=sizes.get(item.get('size')),
                color_id=item.get('color'),
                color=colors.get(item.get('color')),
                count=count,
                price=price,
                subtotal=count * price
            )
            new_basket.append(new_item)
        context['basket'] = new_basket

        return context


class BacketRemoveView(View):
    def post(self, request, *args, **kwargs):
        product = kwargs.get('product')
        try:
            color = int(request.POST.get('color'))
        except:
            color = None
        try:
            size = int(request.POST.get('size'))
        except:
            size = None
        basket = self.request.session.get('basket', [])
        for i in range(len(basket)):
            if basket[i]['product'] == product and basket[i]['color'] == color and basket[i]['size'] == size:
                del basket[i] 
                break
        self.request.session['basket'] = basket
        self.request.session.modified = True
        return redirect(reverse('basket_index'))
