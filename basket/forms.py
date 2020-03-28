from django import forms


class BasketAddForm(forms.Form):
    product = forms.IntegerField()
    color = forms.IntegerField(required=False)
    size = forms.IntegerField(required=False)
