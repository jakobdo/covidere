from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import (PhoneNumberInternationalFallbackWidget,
                                       PhoneNumberPrefixWidget)

from order.models import Order
from product.models import Product
from shop.models import Shop

#from intl_tel_input.widgets import IntlTelInputWidget



class ShopContactForm(forms.Form):
    email = forms.EmailField(label=gettext_lazy('email'), required=True)
    subject = forms.CharField(label=gettext_lazy('subject'), required=True)
    message = forms.CharField(label=gettext_lazy('message'), widget=forms.Textarea, required=True)


class ShopRegisterForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'email', 'phone']
        #widgets = {'phone': PhoneNumberPrefixWidget(initial='DK',attrs={'class': 'form-control'})} # 'initial' not working in package 
        widgets = {'phone': PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control'})}

class ShopProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'offer_price', 'active', 'delivery_days', 'start_datetime', 'end_datetime']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ShopProductForm, self).__init__(*args, **kwargs)
    

    def clean(self):
        # Limitation - A customer can have 3 active products
        limit = 3
        if self.instance:
            active_products = Product.objects.filter(active=True, shop=self.request.user.shop).exclude(pk=self.instance.pk).count()
        else:
            active_products = Product.objects.filter(active=True, shop=self.request.user.shop).count()
        if self.cleaned_data.get('active', False) and active_products >= limit:
            raise ValidationError(gettext("Maximum of %(limit)s products reached!") % {'limit': limit})


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
