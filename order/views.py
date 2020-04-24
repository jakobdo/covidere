from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
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

    def form_valid(self, form):
        self.object = form.save()

        # Fetch all products
        basket = self.request.session.get('basket', [])
        products_in_basket = [item.get('product') for item in basket]
        products = Product.objects.filter(pk__in=products_in_basket, active=True, shop__active=True)
        products_dict = {product.pk: product for product in products}

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


        #current_site = get_current_site(self.request)
        subject = gettext('FOODBEE - Order confirmation')
        message = render_to_string('emails/order_confirmation.html', {
            'order' : self.object, # order.models.Order
            'products' : products, # list of product.models.Product 
        })

        # TODO: Should be 1 email per shop you have ordered from, because customers may contact shop with the email
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[self.object.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
        )
        # Clear session
        del self.request.session['basket']
        return HttpResponseRedirect(self.get_success_url())


class OrderCreatedView(TemplateView):
    """
    Order is created view, Thanks to customer
    """
    template_name = 'order/thanks.html'
