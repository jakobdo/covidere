import pytest

from basket.forms import BasketAddForm


class TestBasketAddForm:
    form_class = BasketAddForm

    @pytest.mark.parametrize(
        'product, count, validity',
        [
            (1, None, True),
            ('1', None, True),
            (1, 1, True),
            (1, 0, False),
            (None, None, False),
            (None, 1, False),
            (None, 0, False),
        ]
    )
    def test_form(self, product, count, validity):
        data = {
            'product': product,
            'count': count,
        }
        form = self.form_class(data)
        assert form.is_valid() == validity
