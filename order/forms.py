from django import forms

from order.models import Order
from postcode.models import Postcode

class OrderForm(forms.ModelForm):
    terms = forms.BooleanField(label='Jeg accepterer at jeg handler direkte med butikken, og min bestilling er først endelig når betalingen er gennemført, og butikken har bekræftet.', required=True)

    class Meta:
        model = Order
        fields = ['name', 'address', 'postcode', 'email', 'mobile', 'terms']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['postcode'].queryset = Postcode.objects.filter(active=True)