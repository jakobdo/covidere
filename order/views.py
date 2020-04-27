from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, TemplateView
from decimal import Decimal
from django.template import Context

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

    def form_valid(self, form):
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
                'total_cost' : Decimal(0.00), 
                'order_items' : [],
                'item_count' : 0
            }

        # Create orderItems
        for item in basket:
            product = products_dict[item.get('product')]
            color = item.get('color')
            size = item.get('size')
            count = item.get('count')
            # If product is not found, skip product
            if product is None:
                continue

            # If count is 0 or below, skip item
            if count < 1:
                continue

            # if right color in item
            if color and not product.color.filter(pk=color):
                continue
        
            # if right size in item
            if size and not product.size.filter(pk=size):
                continue

            order_item = OrderItem()
            order_item.product = product
            if color:
                order_item.color_id = color
            if size:
                order_item.size_id = size
            order_item.order = self.object
            order_item.count = count
            # Save the offer/on sale price if any, else use normal price
            order_item.price = product.offer_price if product.offer_price else product.price
            order_item.save()

            shop_items_and_cost[product.shop]['item_count'] += count
            shop_items_and_cost[product.shop]['total_cost'] += Decimal(count * product.price)
            shop_items_and_cost[product.shop]['order_items'].append(order_item) 

        context = {
            'order' : self.object, 
            'shop_items_and_cost': shop_items_and_cost
        }
        message = render_to_string('emails/order_confirmation.txt', context)
        html_message = render_to_string('emails/order_confirmation.html', context)
        subject = gettext('Order confirmation')

        self.object.status = Order.ORDERED

        # TODO: Should be 1 email per shop you have ordered from, because customers may contact shop with the email
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[self.object.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
            html_message=html_message,
        )

        # Clear session
        self.request.session.flush()
        return HttpResponseRedirect(self.get_success_url())


class OrderCreatedView(TemplateView):
    """
    Order is created view, Thanks to customer
    """
    template_name = 'order/thanks.html'
