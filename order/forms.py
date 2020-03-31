from django import forms

from order.models import Order


class OrderForm(forms.ModelForm):
    terms = forms.BooleanField(label='Jeg accepterer at jeg handler direkte med butikken, og min bestilling er først endelig når betalingen er gennemført, og butikken har bekræftet.', required=True)


    class Meta:
        model = Order
        fields = ['name', 'address', 'zipcode', 'city', 'email', 'mobile', 'terms']
