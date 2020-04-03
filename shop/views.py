from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import DetailView, FormView, ListView

from shop.forms import ShopContactForm
from shop.models import Shop


class ShopsListView(ListView):
    """
    Shop List View. Will list all active shops for enduser
    """
    model = Shop
    template_name = 'shop/list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(active=True)
        return queryset


class ShopsDetailView(DetailView):
    """
    Shop Detail View. Will show detail for an active shop
    """
    model = Shop
    template_name = 'shop/detail.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(active=True)
        return queryset


class ShopContactView(SuccessMessageMixin, FormView):
    """
    Contact shop form. Will send an email to the shop contact
    """
    template_name = 'shop/contact.html'
    form_class = ShopContactForm
    success_message = gettext_lazy("Message sent to shop, they will get in touch.")

    def get_success_url(self):
        return reverse('shop_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))
        send_mail(
            subject=form.cleaned_data.get('subject'),
            message=form.cleaned_data.get('message'),
            from_email=form.cleaned_data.get('email'),
            recipient_list=[shop.email],
            fail_silently=False,
        )
        return super().form_valid(form)
