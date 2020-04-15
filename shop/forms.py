from django import forms
from django.contrib.auth import password_validation
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy

from product.models import Product
from shop.models import Postcode, Shop


class ShopContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ShopRegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': gettext_lazy('The two password fields didn’t match.'),
    }

    username = forms.EmailField(label=gettext_lazy("User email"),)
    password1 = forms.CharField(
        label=gettext_lazy("Password"),
        strip=False,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=gettext_lazy("Password confirmation"),
        widget=forms.PasswordInput(),
        strip=False,
        help_text=gettext_lazy("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Shop
        fields = ['name', 'address', 'postcode', 'email', 'homepage', 'phone', 'delivery_postcode', 'username', 'password1', 'password2']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class ShopProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'offer_price', 'color', 'size', 'active', 'delivery_days', 'start_datetime', 'end_datetime']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ShopProductForm, self).__init__(*args, **kwargs)
    

    def clean(self):
        # Limitation - A customer can have 3 active products
        limit = 3
        if self.cleaned_data.get('active', False) and Product.objects.filter(active=True, shop=self.request.user.shop).count() >= limit:
            raise ValidationError(gettext("Maximum of %(limit)s products reached!") % {'limit': limit})


class PostCodeForm(forms.ModelForm):
    class Meta:
        model = Postcode
        fields = ['postcode']