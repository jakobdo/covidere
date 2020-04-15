from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy


class DriverRegisterForm(forms.ModelForm):

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