from django.http import HttpRequest

from base.processors import basket_counter


class TestBasketCounter:
    def test_basket_counter_context(self):
        request = HttpRequest()
        request.session = {}
        context = basket_counter(request)
        assert context['basket_counter'] == 0
