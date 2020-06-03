from django import forms
from django.utils.translation import gettext_lazy

from postcode.models import Postcode


class PostCodeForm(forms.Form):
    postcode = forms.ModelChoiceField(
        label=gettext_lazy('postcode'),
        queryset=Postcode.objects.filter(active=True),
        to_field_name="postcode"
    )
