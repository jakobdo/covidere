from django import forms

from order.models import Order
from postcode.models import Postcode

class OrderForm(forms.ModelForm):
    postcode = forms.ModelChoiceField(
        queryset=Postcode.objects.filter(active=True),
        widget=forms.HiddenInput
    )
    terms = forms.BooleanField(label='Jeg accepterer at jeg handler direkte med butikken, og min bestilling er først endelig når betalingen er gennemført, og butikken har bekræftet.', required=True)

    class Meta:
        model = Order
        fields = ['name', 'address', 'postcode', 'email', 'mobile', 'terms']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if not isinstance(self.fields[f].widget, forms.CheckboxInput):
                self.fields[f].widget.attrs['placeholder'] = self.fields[f].label
                self.fields[f].label = ''