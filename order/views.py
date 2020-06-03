from decimal import Decimal
from email.mime.image import MIMEImage

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, TemplateView

from order.forms import OrderForm
from order.models import Order, OrderItem
from product.models import Product


class OrderCreateView(CreateView):
    """
    Order Create View
    """
    model = Order
    template_name = 'order/create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_thanks')

    def get_context_data(self, **kwargs):
        kwargs['sitekey'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # TODO - Move to own implementation
        # Validate Google Recaptcha V3
        response = form.data.get('g-recaptcha-response')
        data = {
            'response': response,
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY
        }
        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )
        result = resp.json()
        if not result['success'] or not result['action'] == 'order':
            form.add_error(None, gettext("Invalid recaptcha response, please try again."))
            return super().form_invalid(form)

        self.object = form.save()

        # Fetch all products
        basket = self.request.session.get('basket', [])
        products_in_basket = [item.get('product') for item in basket]
        products = Product.objects.filter(pk__in=products_in_basket, active=True, shop__active=True).order_by('shop')
        products_dict = {product.pk: product for product in products}

        # Total cost & valid items list per shop
        shop_items_and_cost = dict.fromkeys({product.shop for product in products})
        for key in shop_items_and_cost:
            shop_items_and_cost[key] = {
                'total_cost': Decimal(0.00),
                'order_items': [],
                'item_count': 0
            }

        # Create orderItems
        for item in basket:
            product = products_dict[item.get('product')]
            count = item.get('count')
            # If product is not found, skip product
            if product is None:
                continue

            # If count is 0 or below, skip item
            if count < 1:
                continue

            order_item = OrderItem()
            order_item.product = product
            order_item.order = self.object
            order_item.count = count
            # Save the offer/on sale price if any, else use normal price
            order_item.price = product.offer_price if product.offer_price else product.price
            order_item.save()

            shop_items_and_cost[product.shop]['item_count'] += count
            shop_items_and_cost[product.shop]['total_cost'] += Decimal(order_item.subtotal())
            shop_items_and_cost[product.shop]['order_items'].append(order_item)

        context = {
            'order': self.object,
            'shop_items_and_cost': shop_items_and_cost
        }
        html_message = render_to_string('emails/order_confirmation.html', context)
        txt_message = render_to_string('emails/order_confirmation.txt', context)
        subject = gettext('Order confirmation')

        self.object.status = Order.ORDERED

        email = EmailMultiAlternatives(subject, txt_message)
        email.from_email = settings.DEFAULT_FROM_EMAIL
        email.to = [self.object.email]
        email.attach_alternative(html_message, "text/html")
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'

        with open('base/static/base/img/fb_logo.png', mode='rb') as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', "<Foodbee_logo_long.png>")
            email.attach(image)

        email.send()

        # Clear session
        self.request.session.flush()
        return HttpResponseRedirect(self.get_success_url())


class OrderCreatedView(TemplateView):
    """
    Order is created view, Thanks to customer
    """
    template_name = 'order/thanks.html'
