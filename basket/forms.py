from django import forms


class BasketAddForm(forms.Form):
    product = forms.IntegerField()
    count = forms.IntegerField(min_value=1, required=False)

    def clean_count(self):
        count = self.cleaned_data.get('count')
        if count is None:
            return 1
        else:
            return count
