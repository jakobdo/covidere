from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext
from django.views import View
from django.views.generic import FormView, TemplateView

from basket.forms import BasketAddForm
from basket.utils import Basket
from product.models import Product


class BasketAddView(View):
    def post(self, request, *args, **kwargs):
        form = BasketAddForm(request.POST)
        if form.is_valid():
            basket = Basket(self.request.session)
            self.request.session['basket'] = basket.add(
                form.cleaned_data.get('product'),
                form.cleaned_data.get('count'),
            )
            self.request.session.modified = True
            #messages.add_message(self.request, messages.INFO, gettext('Product added to basket'))
            return JsonResponse({
                'msg': gettext('Product added to basket'), 
                'count': basket.count(),
            })
        else:
            return JsonResponse({'msg': gettext('Product not added to basket')}, status=400)


class BasketIndexView(TemplateView):
    template_name = "basket/list.html"

    def get_context_data(self, **kwargs):
        context = super(BasketIndexView, self).get_context_data(**kwargs)
        basket = self.request.session.get('basket', [])

        # Load products
        products = {p.id: p for p in Product.objects.filter(
            pk__in=[item.get('product') for item in basket]
        ).select_related('shop')}

        new_basket = []
        total = 0

        for item in basket:
            count = item.get('count')
            price = products.get(item.get('product')).get_price()
            subtotal = count * price
            new_item = dict(
                product_id=item.get('product'),
                product=products.get(item.get('product')).name,
                shop=products.get(item.get('product')).shop.name,
                count=count,
                price=price,
                subtotal=subtotal
            )
            new_basket.append(new_item)
            total += subtotal
        basket = sorted(new_basket, key=lambda item: item['product'])
        basket = sorted(basket, key=lambda item: item['shop'])
        context['basket'] = basket
        context['total'] = total
        return context


class BasketUpdateView(View):
    def post(self, request):
        action = request.POST.get('action')
        if action == 'update' or action == 'order':
            basket = request.session.get('basket', [])
            # Loop count elements and update session
            for item in request.POST:
                if item.startswith('count_'):
                    parts = item.split("_")[1:]
                    product = int(parts[0])

                    for i in range(len(basket)):
                        if basket[i]['product'] == product:
                            try:
                                count = int(request.POST.get(item))
                            except (TypeError, ValueError):
                                count = 0
                            if count > 0:
                                basket[i]['count'] = count
                            else:
                                del basket[i] 
                            break
            request.session['basket'] = basket
            request.session.modified = True

            if action == 'order':
                return redirect(reverse('order'))
            else:
                messages.add_message(self.request, messages.INFO, gettext('Basket updated'))
        elif action == 'clear':
            request.session['basket'] = []
            request.session.modified = True
            messages.add_message(self.request, messages.INFO, gettext('Basket cleared'))
        elif action.startswith('remove_'):
            parts = action.split("_")[1:]
            product = int(parts[0])
            basket = request.session.get('basket', [])
            for i in range(len(basket)):
                if basket[i]['product'] == product:
                    del basket[i]
                    messages.add_message(self.request, messages.INFO, gettext('Product removed from basket'))
                    break
            request.session['basket'] = basket
            request.session.modified = True
        return redirect(reverse('basket_index'))
